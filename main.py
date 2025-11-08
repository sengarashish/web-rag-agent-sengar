#!/usr/bin/env python3

import sys
from src.utils.config_loader import load_config, get_urls, get_request_delay
from src.loaders.web_scraper import WebScraper
from src.loaders.vector_store import VectorStoreManager
from src.agents.rag_agent import RAGAgent

def main():
    print("=" * 60)
    print("Web RAG Agent - Interactive Q&A by Sengar")
    print("=" * 60)
    
    # load config
    try:
        config = load_config()
    except Exception as e:
        print(f"Error loading config: {e}")
        sys.exit(1)
    
    api_key = config.get('GEMINI_API_KEY', '')
    if not api_key or api_key == 'your_api_key_here':
        print("Error: Please set GEMINI_API_KEY in config.properties")
        sys.exit(1)
    
    urls = get_urls(config)
    if not urls:
        print("Error: No URLs configured")
        sys.exit(1)
    
    delay = get_request_delay(config)
    model_name = config.get('MODEL_NAME', 'gemini-1.5-flash')
    chunk_size = int(config.get('CHUNK_SIZE', 1000))
    chunk_overlap = int(config.get('CHUNK_OVERLAP', 200))
    
    print(f"\nConfiguration:")
    print(f"  - Model: {model_name}")
    print(f"  - URLs to scrape: {len(urls)}")
    print(f"  - Rate limit delay: {delay}s")
    print()
    
    # scrape URLs
    scraper = WebScraper(delay=delay)
    scraped_data = scraper.scrape_urls(urls)
    
    # build vector store
    vector_store = VectorStoreManager(
        api_key=api_key,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    
    try:
        vector_store.build_index(scraped_data)
    except Exception as e:
        print(f"Error building index: {e}")
        sys.exit(1)
    
    # initialize agent
    agent = RAGAgent(
        api_key=api_key,
        model_name=model_name,
        vector_store=vector_store
    )
    
    print("\n" + "=" * 60)
    print("Ready! Ask me anything (type 'exit' or 'quit' to stop)")
    print("=" * 60 + "\n")
    
    # interactive loop
    while True:
        try:
            query = input("You: ").strip()
            
            if not query:
                continue
            
            if query.lower() in ['exit', 'quit', 'q']:
                print("Goodbye!")
                break
            
            print("\nThinking...\n")
            response = agent.run(query)
            print(f"Agent: {response}\n")
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}\n")

if __name__ == "__main__":
    main()
