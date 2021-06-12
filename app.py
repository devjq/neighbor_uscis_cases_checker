from flask import Flask, request, render_template, redirect, url_for
from utils import get_status

app = Flask(__name__)
app.config["CACHE_TYPE"] = "null"


@app.route('/',methods=['GET','POST'])
def index():
    if request.method =='POST':
        cnum = request.form['cnum']
        n_count = request.form['n_count']
        return redirect(url_for("case", case_num=cnum, n_count=n_count))
    return render_template('input.html')

# Show a loading gif for long running task
# https://stackoverflow.com/questions/42805765/how-to-add-a-loading-gif-to-the-page-when-a-function-runs-in-the-background-in-f

@app.route('/case/<case_num>')
def case(case_num, n_count=10):
    status_dict = {
        'case_num': [],
        'case_date': [],
        'form': [],
        'status': []
    }
    int_case_num = int(case_num[3:])
    prefix = case_num[:3]

    try:
        passed_n_count = int(request.args['n_count'])
        n_count = min(passed_n_count, n_count)
    except:
        pass

    for cnum in range(int_case_num-n_count, int_case_num+n_count+1):
        cnum, cdate, form, status = get_status(case_num=prefix+str(cnum))
        status_dict['case_num'].append(cnum)
        status_dict['case_date'].append(cdate)
        status_dict['form'].append(form)
        status_dict['status'].append(status)

    status_dict = zip(status_dict['case_num'],
                      status_dict['case_date'],
                      status_dict['form'],
                      status_dict['status'])
    return render_template('index.html',
                           status=status_dict)


if __name__ == "__main__":
    # app.run(debug=True, port=8080)
    app.run(port=8080)
