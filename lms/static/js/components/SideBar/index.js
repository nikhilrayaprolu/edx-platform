import React from 'react';
import ReactDOM from 'react-dom';
import {BrowserRouter} from "react-router-dom/";
import '../../scss/index.scss';

class SideBar extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            error: null,
            isLoaded: false,
            username: '',
            first_name: '',
            email: '',
            followers: '',
            following: '',
        };
    }
    componentDidMount() {
        fetch("/youngwall/follow_count")
            .then(res => res.json())
            .then(
                (result) => {
                    this.setState({
                        isLoaded: true,
                        username: result.username,
                        first_name: result.first_name,
                        email: result.email,
                        followers: result.followers,
                        following: result.following,
                    });
                },
                (error) => {
                    this.setState({
                        isLoaded: true,
                        error
                    })
                }
            )
    }
    render () {
        const { error, isLoaded, username, first_name, email, followers, following} = this.state;
        console.log("came into sidebar");
        return (
            <React.Fragment>
                <div className="row">
                    <div className="col-md-3">
                    <aside className="profile-sidebar">
                        <h2>Account Details</h2>
                        <header className="profile">
                            <h1 className="user-name break-word">{username}</h1>
                        </header>
                        <section className="user-info">
                            <ul>
                                <li className="info--username">
                                    <span className="title">Full Name</span>
                                    <span className="data break-word">{first_name}</span>
                                </li>

                                <li className="info--email">
                            <span className="title">
                              Email
                            </span>
                                    <span className="data break-word">
                                        {email}
                            </span>
                                </li>
                                <li className="info--Followers" >
                                    <a href="/youngwall/myfollowers">
                            <span className="title">
                              Followers
                            </span>
                                    <span className="data break-word">
                              Count: {followers}
                            </span>
                                        </a>
                                </li>
                                <li className="info--Followers">
                                    <a href="/youngwall/friends">
                            <span className="title">
                              Following
                            </span>
                                    <span className="data break-word">
                              Count: {following}
                            </span>
                                        </a>
                                </li>
                                <li className="controls--account">
                                </li>
                            </ul>
                        </section>
                    </aside>
                    </div>
            </div>
            </React.Fragment>

        )
    }
}
export default SideBar
ReactDOM.render(
      <SideBar />
    ,
      document.getElementById('side-bar'),
    );
