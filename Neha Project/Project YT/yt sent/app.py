from flask import Flask, render_template, request
import os
from Youtubesenti import extract_video_id,analyze_sentiment,generate_bar_chart,generate_pie_chart,generate_suggested_comments
from ytscrapper import (save_video_comments_to_csv,
                                    get_channel_info,
                                    youtube,
                                    get_channel_id,
                                    get_video_stats   )

app = Flask(__name__)



def delete_non_matching_csv_files(directory_path, video_id):
    for file_name in os.listdir(directory_path):
        if not file_name.endswith('.csv'):
            continue
        if file_name == f'{video_id}.csv':
            continue
        os.remove(os.path.join(directory_path, file_name))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        youtube_link = request.form['youtube_link']
        video_id = extract_video_id(youtube_link)
        channel_id = get_channel_id(video_id)
        

        if video_id:
            # Define directory_path here
            directory_path = os.getcwd()  

            csv_file = save_video_comments_to_csv(video_id)
            delete_non_matching_csv_files(directory_path, video_id)

            channel_info = get_channel_info(youtube, channel_id)
            stats = get_video_stats(video_id)
            comments,results = analyze_sentiment(csv_file)
            suggested_comments = generate_suggested_comments(comments)

            # Generate HTML strings for charts
            bar_chart_image = generate_bar_chart(results)
            pie_chart_image = generate_pie_chart(results)
            return render_template('index.html',
                                    video_id = video_id,
                                   channel_info=channel_info,
                                   stats=stats,
                                   results=results,
                                   bar_chart_image=bar_chart_image,  
                                   pie_chart_image=pie_chart_image,suggested_comments=suggested_comments)  
        else:
            return render_template('index.html', error="Invalid YouTube link")

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
