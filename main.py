import streamlit as st
import language_tool_python
from textblob import TextBlob
import json
from collections import Counter

class GrammarChecker:
    def __init__(self):
        self.tool = language_tool_python.LanguageTool('en-US')
        
    def check_grammar(self, text):
        matches = self.tool.check(text)
        return matches
    
    def get_suggestions(self, match):
        return match.replacements if match.replacements else ["No suggestions available"]
    
    def analyze_text(self, text):
        blob = TextBlob(text)
        return {
            'sentiment': blob.sentiment.polarity,
            'word_count': len(text.split()),
            'char_count': len(text),
            'sentence_count': len(blob.sentences)
        }

def main():
    st.title("📝 Advanced Grammar Checker")
    st.write("Check your text for grammar, spelling, and style issues")
    
    # Initialize the checker
    if 'checker' not in st.session_state:
        st.session_state.checker = GrammarChecker()
    
    # Text input area
    text_input = st.text_area("Enter your text here:", height=200)
    
    if st.button("Check Grammar"):
        if text_input.strip():
            # Grammar checking
            matches = st.session_state.checker.check_grammar(text_input)
            
            # Text analysis
            analysis = st.session_state.checker.analyze_text(text_input)
            
            # Display text statistics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Word Count", analysis['word_count'])
            with col2:
                st.metric("Character Count", analysis['char_count'])
            with col3:
                st.metric("Sentence Count", analysis['sentence_count'])
            with col4:
                sentiment = "Positive" if analysis['sentiment'] > 0 else "Negative" if analysis['sentiment'] < 0 else "Neutral"
                st.metric("Sentiment", sentiment)
            
            # Display grammar issues
            st.header("Grammar Issues Found")
            if matches:
                for i, match in enumerate(matches, 1):
                    with st.expander(f"Issue #{i}: {match.message[:100]}..."):
                        st.write("**Context:** ", match.context)
                        st.write("**Category:** ", match.category)
                        st.write("**Suggested Corrections:**")
                        suggestions = st.session_state.checker.get_suggestions(match)
                        for j, suggestion in enumerate(suggestions[:5], 1):
                            st.write(f"{j}. {suggestion}")
                        
                st.info(f"Found {len(matches)} potential issues in your text.")
            else:
                st.success("No grammar issues found!")
            
            # Word frequency analysis
            st.header("Word Frequency Analysis")
            words = text_input.lower().split()
            word_freq = Counter(words)
            common_words = dict(word_freq.most_common(10))
            
            # Create bar chart of word frequency
            st.bar_chart(common_words)
            
    # Tips section
    with st.expander("Writing Tips"):
        st.write("""
        ### Tips for Better Writing
        1. **Use Active Voice:** Active voice makes your writing clearer and more direct
        2. **Be Concise:** Remove unnecessary words and repetition
        3. **Check Punctuation:** Pay attention to commas, periods, and other punctuation marks
        4. **Use Transition Words:** Help your readers follow your thoughts with good transitions
        5. **Proofread:** Always review your text before finalizing
        """)

if __name__ == "__main__":
    main()