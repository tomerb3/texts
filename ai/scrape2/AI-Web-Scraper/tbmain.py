import streamlit as st
from web_scrape import scrape_website, split_dom_content, clean_body_content, extract_body_content
from parse import parse_with_ollama

#Contains UI


#url = 'https://github.com/NotHarshhaa/DevOps-Projects'
#url ='https://site.financialmodelingprep.com/developer/docs#Stock-News'
#url ='https://finance.yahoo.com/topic/stock-market-news/'
url='https://www.investopedia.com/dow-jones-today-03142025-11696887'
result = scrape_website(url)
body_content = extract_body_content(result)
cleaned_content = clean_body_content(body_content)
    
st.session_state.dom_content = cleaned_content #store data in session to use it later
 
with st.expander("View DOM Content"):
        st.text_area("DOM Content", cleaned_content, height=300)
        

if "dom_content" in st.session_state:
    #parse_decription = "Explain me this website"
    parse_decription = "explain me what stock you love most"
    dom_chunks = split_dom_content(st.session_state.dom_content)
    result = parse_with_ollama(dom_chunks, parse_decription)
    print(result)
