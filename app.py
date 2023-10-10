# Standard Library Imports
from flask import ( Flask, jsonify, render_template, request,
                    url_for,
                    make_response,
                    session,
                    send_file,
                    Response,
                    render_template_string,
                    redirect)
import pandas as pd
import plotly.graph_objects as go
from sqlalchemy import create_engine
from config import tbl_mapping
from data_connector.sqlite_connector import get_db_connection
from lang_assistant.langhelper import chat_response, summary_extractor_from_df, chat_with_df, generate_graphdata
from utilities.plotting import (get_validation_json, 
                                badges_get_pillar_dougnutdata, 
                                badges_get_badgecompletion_monthwise, 
                                get_wfrankwise_countmom, 
                                get_lst_topdepartment, 
                                get_wfrankwise_count,
                                get_topfive_badgetitle)
import sqlite3
import time
import json

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'test'

@app.route("/validate_learning", methods=['GET'])
def load_learning():
    con = sqlite3.connect("database.db")
    df = pd.read_sql_query(f"SELECT * from learning", con)
    no_rows, no_cols = df.shape
    n_gui = df.GUI.nunique() if 'GUI' in df.columns else 'GUI not Found'

    tablevalues = {'n_rows':no_rows, 'n_cols':no_cols, 'unique_gui':n_gui}
    print('Calculation done')
    # Data for the bar chart
    bar_chart_data = {
        'labels': ['Label 1', 'Label 2', 'Label 3', 'Label 4', 'Label 5'],
        'values': [30, 40, 30, 21, 34]
    }
    # Data for the pie chart
    pie_chart_data = {
        'labels': ['Label A', 'Label B', 'Label C', 'Label D', 'Label E'],
        'values': [45, 30, 25, 9, 34]
    }

    # Create the bar chart figure
    bar_chart_figure = go.Figure(
        data=[
            go.Bar(
                x=bar_chart_data['labels'],
                y=bar_chart_data['values'],
                marker_color='rgba(54, 162, 235, 0.5)',
                marker_line_color='rgba(54, 162, 235, 1)',
                marker_line_width=1
            )
        ],
        layout=go.Layout(
            title='Bar Chart',
            yaxis=dict(title='Values'),
            margin=dict(l=20, r=20, t=40, b=20)
        )
    )

    # Create the pie chart figure
    pie_chart_figure = go.Figure(
        data=[
            go.Pie(
                labels=pie_chart_data['labels'],
                values=pie_chart_data['values'],
                hole=0.3,
                marker=dict(colors=['rgba(255, 99, 132, 0.5)', 'rgba(54, 162, 235, 0.5)', 'rgba(255, 206, 86, 0.5)'],
                            line=dict(color='rgba(0, 0, 0, 0.5)', width=1))
            )
        ],
        layout=go.Layout(
            title='Pie Chart',
            margin=dict(l=20, r=20, t=40, b=20)
        )
    )
    # Convert the figures to HTML
    bar_chart_html = bar_chart_figure.to_html(full_html=False)
    pie_chart_html = pie_chart_figure.to_html(full_html=False)

    data = {
        'Regex issue': [-90, -10, -5, 0],
        'Null percentage': [-10, -35, 0, 0],
        'Seems ok': [40, 45, 90, 100],
        'data mismatch': [0, -10, -5, 0]
    }

    df = pd.DataFrame(data, index=['GTE', 'SMU', 'Service_Line', 'Sub_SL'])

    labels = df.index.to_list()
    reg_issue = df['Regex issue'].to_list()
    null_issue = df['Null percentage'].to_list()
    ok_data = df['Seems ok'].to_list()
    mismatch_issue = df['data mismatch'].to_list()
    tbl_selected = session.get('tbl_selected', [])

    return render_template("validate_learning.html",
                            req_tables = tbl_selected,
                            bar_chart_html=bar_chart_html, 
                            pie_chart_html=pie_chart_html, 
                            table_info = tablevalues,
                            labels = labels, reg_issue=reg_issue, 
                            null_issue=null_issue, ok_data=ok_data , mismatch_issue=mismatch_issue,
                            show_sidebar=True)

@app.route("/validate_badges", methods=['GET', 'POST'])
def load_badges():
    con = sqlite3.connect("database.db")
    df = pd.read_sql_query(f"SELECT * from badges", con)
    no_rows, no_cols = df.shape
    n_gui = df.GUI.nunique() if 'GUI' in df.columns else 'GUI not Found'

    tablevalues = {'n_rows':no_rows, 'n_cols':no_cols, 'unique_gui':n_gui}
    print('Calculation done')
    
    tbl_selected = session.get('tbl_selected', [])

    json_data = get_validation_json('badges')
    json_pillar_data = badges_get_pillar_dougnutdata()
    json_badgecompletion_data = badges_get_badgecompletion_monthwise()
    lst_topfive_badgetitle = get_topfive_badgetitle()
    
    return render_template("validate_badges.html",
                            lst_topfive_badgetitle = lst_topfive_badgetitle,
                            req_tables = tbl_selected,
                            table_info = tablevalues,
                            json_data = json_data,
                            json_pillar_data=json_pillar_data,
                            json_badgecompletion_data = json_badgecompletion_data,
                            show_sidebar=True)

@app.route("/validation", methods=['GET', 'POST'])
@app.route("/validate_workforce", methods=['GET', 'POST'])
def load_workforce():
    con = sqlite3.connect("database.db")
    df = pd.read_sql_query(f"SELECT * from workforce", con)
    no_rows, no_cols = df.shape
    n_gui = df.GUI.nunique() if 'GUI' in df.columns else 'GUI not Found'

    tablevalues = {'n_rows':no_rows, 'n_cols':no_cols, 'unique_gui':n_gui}
    
    json_val_data = get_validation_json('workforce')
    json_empdist = get_wfrankwise_countmom()
    lst_topfive_dept = get_lst_topdepartment()
    json_rankwise_empdist = get_wfrankwise_count()
    tbl_selected = session.get('tbl_selected', []) #['Badges', 'learning']
    gpt_response = summary_extractor_from_df("""{"male": 56, "female": 44 }""")

    return render_template("validate_workforce.html",
                            req_tables = tbl_selected,
                            table_info = tablevalues,
                            json_data = json_val_data,
                            json_empdist = json_empdist,
                            lst_topfive_dept = lst_topfive_dept,
                            json_rankwise_empdist = json_rankwise_empdist,
                            aicontent_genderanalysis = gpt_response, 
                            show_sidebar = True)

@app.route("/validate_miscellaneous", methods=['GET', 'POST'])
def load_miscellaneous():
    tbl_selected = session.get('tbl_selected', [])    
    return render_template("validate_miscellaneous.html", 
                           req_tables = tbl_selected,
                           show_sidebar = True)

@app.route("/timecard.html", methods=['GET', 'POST'])
def load_timecard():
    return render_template("timecard.html")

@app.route("/get_llmresponse")
def get_bot_response():
    user_message = request.args.get('msg')
    dd_table_selected = request.args.get('table_selected')
    print(f"user message and table selected : {user_message}, {dd_table_selected}")
    print(f"request args : {request.args.get('msg')}")
    response_usrmsg = chat_with_df(user_message, table_name = dd_table_selected)
    return response_usrmsg

@app.route("/get_val_llmresponse")
def get_bot_valresponse():
    user_message = request.args.get('msg')
    table_selected = request.args.get('table_selected')
    print(f"user message and table selected : {user_message}, {table_selected}")
    print(f"request args : {request.args.get('msg')}")

    try:
        llm_response_dict = generate_graphdata(user_message, table_name = table_selected)
    except Exception as e:
        llm_response_dict = dict(success=False, 
                                chart_type='text', 
                                chart_label=None,
                                chart_json_data=None,
                                text_to_display="Exception : Some error occured while processing, "+str(e)[:50] + "..")
    
    print(llm_response_dict)
    output_gendata = json.dumps(llm_response_dict)
    return output_gendata

@app.route("/data.html", methods=['GET', 'POST'])
@app.route("/data", methods=['GET', 'POST'])
def data():
    tbl_htmls = {}
    tbl_selected = session.get('tbl_selected', [])
    print(tbl_selected)
    for tblname in tbl_selected:
        # Read sqlite query results into a pandas DataFrame
        con = sqlite3.connect("database.db")
        df = pd.read_sql_query(f"SELECT * from {tblname}", con)
        top_records = df.copy()
        con.close()
        html_top_records = top_records.to_html(index=False, table_id= f'dtable_{tblname}', classes='display nowrap table table-bordered table-striped table-condensed small p-1', justify='left')
        html_top_records = html_top_records.replace('<thead>', '<thead class="thead-light" style="top: 0;position: sticky;">')
        tbl_htmls[tblname] = html_top_records

    return render_template('data.html', table_htmls = tbl_htmls, req_tables = json.dumps(tbl_selected[0]))

@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def hometest():
    if request.method == 'GET':
        return render_template('home.html')
    elif request.method == 'POST':
        session['start_date'] = request.form.get('calendar_value').split(":")[0]
        session['end_date'] = request.form.get('calendar_value').split(":")[1]
        session['sl_subsl'] = request.form.get('sl_subsl')
        session['tbl_selected'] = request.form.getlist('tbl_selected')
        return redirect(url_for('data'))

if __name__ == '__main__':
    #app.run(debug=True)
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)
