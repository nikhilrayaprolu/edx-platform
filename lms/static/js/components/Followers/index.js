import React from 'react';
import FollowButton from "../followbutton";
import {handlefollow} from "../../utils";


export default class Followers extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            error: null,
            isLoaded: false,
            following_followers: [],
            non_following_followers: [],
            userid: null,
        };
        this.handlefollow = this.handlefollow.bind(this)
    }
    componentDidMount() {
        fetch("/youngwall/followerslist")
            .then(res => res.json())
            .then(
                (result) => {
                    this.setState({
                        isLoaded: true,
                        following_followers: result.following_followers,
                        non_following_followers: result.non_following_followers,
                        userid: result.userid
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
    handlefollow(id) {
        handlefollow(this.state.userid, id, 'user');
    }
    displayitem(item, follow) {
        return (
            <div className="col-md-12 border-bottom" key={item.pk}>
                <div className="row">
                    <div className="col-md-2">
                        <a href={"/" + item.username}>
                        <div id="profileImage">{item.username[0]}</div>
                        </a>
                    </div>
                    <div className="col-md-6">
                        <h4><a href={"/" + item.username}>{item.name}</a></h4>
                        <p>School: {item.schoolname}<br/>
                        Class: {item.classname}<br/>
                        Section: {item.section}</p>
                    </div>
                    <div className="col-md-2">
                        <FollowButton followed={follow} clicked={() => this.handlefollow(item.username)}/>
                    </div>
                </div>

            </div>
        )
    }
    render () {
        const { error, isLoaded, following_followers, non_following_followers } = this.state;
        if (error) {
            return <React.Fragment><div>Error: {error.message}</div></React.Fragment>;
        } else if (!isLoaded) {
            return <React.Fragment><div className="container" id="react-feed"><h2>Loading... Friends</h2></div></React.Fragment>;
        } else {
            let followers = "Followers";
            return (
                    <div className="container" id="react-feed">
                        <div className="shadow">
                            <h1>{followers}</h1>
                            <div className="row">
                                {
                                    following_followers.map(item => this.displayitem(item, true))
                                }
                                {
                                    non_following_followers.map(item => this.displayitem(item, false))
                                }
                            </div>
                        </div>
                    </div>
            );
        }
    }
}
