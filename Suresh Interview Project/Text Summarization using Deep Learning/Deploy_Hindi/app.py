# !pip install pyngrok

# Flask utils
from flask import Flask, redirect, url_for, request, render_template
# from pyngrok import ngrok
from TextSummarization_utils import *

import warnings
warnings.filterwarnings('ignore')

# Define a flask app
app = Flask(__name__)

# start ngrok when app is run
# port_no = 5000
# ngrok.set_auth_token("2KdKVvWPZia5YkGnclMcSmJGTjF_7XRGo19n8sau4r29JNaPL")
# public_url = ngrok.connect(port_no).public_url

@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html', flag=False)

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        # Get the file from post request
        text = request.form.get('text')
        number_of_sentences = int(request.form.get('num_sentences'))
        # summary_result = text_summarizer(text, number_of_sentences)
        # print(f"summary_result : {summary_result}")

        clean_sentences = get_clean_sentences(text)
        
        summary_tf_weight = summarise_term_frequency_sentence_weighing(clean_sentences)
        summary_tf_weight_img_path = get_hindi_wordcloud(summary_tf_weight)
        result1 = ["Term frequency and weighting", summary_tf_weight, summary_tf_weight_img_path]

        summary_tf_idf_weight = summarise_tf_idf_sentence_weighting(clean_sentences)
        summary_tf_idf_weight_img_path = get_hindi_wordcloud(summary_tf_idf_weight)
        result2 = ["TFIDF sentence weighting", summary_tf_idf_weight, summary_tf_idf_weight_img_path]

        summary_rule_based = generate_summary_rule_based(clean_sentences,0.4)
        summary_rule_based_img_path = get_hindi_wordcloud(summary_rule_based)
        result3 = ["TFIDF sentence weighting", summary_rule_based, summary_rule_based_img_path]

        # return render_template('index.html', flag=True, summary_result=summary_result)
        return render_template('index.html', flag=True, result1=result1, result2=result2, result3=result3)
    return render_template('index.html', flag=False)

if __name__ == '__main__':
    # print(f"To acces the Gloable link please click {public_url}")
    # app.run(port=port_no)
    app.run(debug=True)
    # app.run()

