import { h, render, Component } from 'preact';
import firebase from 'firebase/app';
import database from 'firebase/database';



const dvdata = window.DEVOLIO_DATA;

// Initialize Firebase
firebase.initializeApp(dvdata.firebaseConfig);

const CSRFToken = document.cookie.replace(/(?:(?:^|.*;\s*)csrftoken\s*\=\s*([^;]*).*$)|^.*$/, "$1");
const sendReply = (data) => {
    return fetch('/q/new_reply', {
                method: 'POST',
                credentials: 'same-origin',
                headers: new Headers({'X-CSRFToken': CSRFToken}),
                body: JSON.stringify(data)
            });
}


class ReplyForm extends Component {
    constructor(props) {
        super(props);
        this.state = {body: '', qid: dvdata.QID};
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleChange = this.handleChange.bind(this);
    }

    handleSubmit(event) {
        event.preventDefault();

        sendReply({body: this.state.body, qid: this.state.qid})
        this.setState({body: ''})

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
                </form>
                );
        } else {
            return (<a class="button" href="#">Login to leave a response!</a>);
        }
    }
}

class App extends Component {
    state =  {replies: []};

    loadReplies() {

        const replies = firebase.database().ref('question-replies/' + dvdata.QID);
        replies.on('value', items => this.setState({replies: items.val()}) );
    }

    componentDidMount() {
        this.loadReplies();
    }

    renderReplies(reps) {
        if (!reps) return;

        return Object.keys(reps).map(key => {
            return (
                <div className="response">
                <strong>{reps[key].user}</strong><br />
                <div dangerouslySetInnerHTML={{__html: reps[key].body}}></div>
                </div>
            );
        });
    }



    render() {
        const reps = this.state.replies;
        return (
            <div className="responses">
                <h3>Responses:</h3>
                <p>Offer your help. Be nice!</p>
                {this.renderReplies(reps)}
                <ReplyForm/>
            </div>
        );
    }
}

render(<App/>, document.getElementById('replies'));
