import { h, render, Component } from 'preact';
import firebase from 'firebase/app';
import database from 'firebase/database';


const dvdata = window.DEVOLIO_DATA;

// Initialize Firebase
firebase.initializeApp(dvdata.firebaseConfig);

const CSRFToken = document.cookie.replace(/(?:(?:^|.*;\s*)csrftoken\s*\=\s*([^;]*).*$)|^.*$/, "$1");
const sendResponse = (data) => {
    return fetch('/new_response', {
                method: 'POST',
                credentials: 'same-origin',
                headers: new Headers({'X-CSRFToken': CSRFToken}),
                body: JSON.stringify(data)
            });
}


class ResponseForm extends Component {
    constructor(props) {
        super(props);
        this.state = {body: '', qid: dvdata.QID, statusMsg: ''};
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleChange = this.handleChange.bind(this);
        this.showRespMsg = this.showRespMsg.bind(this);
    }

    showRespMsg(msg) {
        this.setState({statusMsg: msg})
        setTimeout((msg) => {
            this.setState({statusMsg: ''})
        }, 5000);
    }


    handleSubmit(event) {
        event.preventDefault();
        if (this.state.body.replace(/\s/g,'').length == 0) {
            return this.showRespMsg("Please provide a response.")
        }

        sendResponse({
                body: this.state.body,
                qid: this.state.qid
            }).then(resp => {
                resp.text().then(text => this.showRespMsg(text))
                if (resp.ok) this.setState({body: ''});
            })
    }

    handleChange(event) {
        this.setState({body: event.target.value});
    }

    render() {
        if (dvdata.loggedIn){
            return (
                <form onSubmit={this.handleSubmit}>
                <textarea
                    value={this.state.body}
                    onChange={this.handleChange}
                ></textarea>
                <input type='submit' className="button" value="Submit" />
                <small>{this.state.statusMsg}</small>
                </form>

                );
        } else {
            return (<a
                        class="button"
                        href={"/users/login/?next="+window.location.pathname}>
                        Login to leave a response!
                    </a>);
        }
    }
}

class App extends Component {
    state =  {responses: []};

    loadResponses() {

        const responses = firebase.database().ref('question-responses/' + dvdata.QID);
        responses.on('value', items => this.setState({responses: items.val()}) );
    }

    componentDidMount() {
        this.loadResponses();
    }

    renderResponses(reps) {
        if (!reps) return;

        return Object.keys(reps).map(key => {
            return (
                <div className="response">
                <strong><a href={"/@"+reps[key].user} >{"@"+reps[key].user}</a></strong><br />
                <div dangerouslySetInnerHTML={{__html: reps[key].body}}></div>
                </div>
            );
        });
    }


    render() {
        const reps = this.state.responses;
        return (
            <div className="responses">
                <h3>Responses <span className="green-dot"
                                    title="Updates in real-time">⬤</span></h3>
                <p>Offer your help. Be nice!</p>
                <p>
                <small>You can use <a
                href="https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet"
                target="_blank">Markdown</a>. The thread updates in real-time.
                </small>
                </p>
                {this.renderResponses(reps)}
                <ResponseForm/>
            </div>
        );
    }
}

render(<App/>, document.getElementById('responses-wrapper'));
