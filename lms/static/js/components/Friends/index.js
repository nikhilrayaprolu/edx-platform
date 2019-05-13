import React from 'react';
import FollowButton from "../followbutton";
import {handlefollow} from "../../utils";


export default class Friends extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            error: null,
            isLoaded: false,
            items: [],
            non_friend_items: [],
            following_teachers: [],
            not_following_teachers: [],
            userid: null,
            username: "",
            school: "",
            classLevel: "",
            section: "",
        };
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleChangeschool = this.handleChangeschool.bind(this);
        this.handleChangeclass = this.handleChangeclass.bind(this);
        this.handleChangesection = this.handleChangesection.bind(this);
        this.handleChangeuser = this.handleChangeuser.bind(this);
    }
    componentDidMount() {
        fetch("/youngwall/friendslist")
            .then(res => res.json())
            .then(
                (result) => {
                    this.setState({
                        isLoaded: true,
                        items: result.friends,
                        non_friend_items: result.non_friends,
                        following_teachers: result.following_teachers,
                        not_following_teachers: result.not_following_teachers,
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
    handleSubmit(event) {
        event.preventDefault();
        let q = "/youngwall/search/user?";
        if(this.state.school)
            q += "school=" + this.state.school + "&";
        if(this.state.classLevel)
            q += "class=" + this.state.classLevel + "&";
        if(this.state.section)
            q += "section=" + this.state.section + "&";
        if(this.state.username)
            q += "user=" + this.state.username;
        fetch(q)
            .then(res => res.json())
            .then(
                (result) => {
                    this.setState({
                        isLoaded: true,
                        items: result.friends,
                        non_friend_items: result.non_friends,
                        following_teachers: result.following_teachers,
                        not_following_teachers: result.not_following_teachers,
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
    handleChangeschool(event) {
        this.setState({school: event.target.value});
    }
    handleChangeclass(event) {
        this.setState({classLevel: event.target.value});
    }
    handleChangesection(event) {
        this.setState({section: event.target.value});
    }
    handleChangeuser(event) {
        this.setState({username: event.target.value});
    }
    handlefollow(id) {
        handlefollow(this.state.userid, id, 'user');
    }
    displayitem(item, follow) {
        return (
            <div className="col-md-12 border-bottom" key={item.pk}>
                <div className="row">
                    <div className="col-md-2">
                        <a href={"/youngwall/" + item.username}>
                        <div id="profileImage">{item.name[0]}</div>
                        </a>
                    </div>
                    <div className="col-md-6">
                        <h4><a href={"/youngwall/" + item.username}>{item.name}</a></h4>
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
        const { error, isLoaded, items, non_friend_items, following_teachers, not_following_teachers } = this.state;
        if (error) {
            return <React.Fragment><div>Error: {error.message}</div></React.Fragment>;
        } else if (!isLoaded) {
            return <React.Fragment><div className="container" id="react-feed"><h2>Loading...</h2></div></React.Fragment>;
        } else {
            let friends = "";
            let teachers = "";
            if( items.length!==0 ||  non_friend_items.length!==0)
                friends = "Friends";
            if( following_teachers.length!==0 ||  not_following_teachers.length!==0)
                teachers = "Teachers";
            if(items.length === 0 && non_friend_items.length === 0)
                friends = "No results";
            return (
                    <div className="container" id="react-feed">
                        <div className="searchbar">
                            <form onSubmit={this.handleSubmit}>
                                <div className="form-group">
                                    <input type="text" className="form-control" placeholder="Enter Username" value={this.state.username} onChange={this.handleChangeuser} />
                                </div>
                                <div className="form-group">
                                    <input type="text" className="form-control" placeholder="Enter School" value={this.state.school} onChange={this.handleChangeschool} />
                                </div>
                                <div className="select-container">
                                    <div className="form-group">
                                        <label htmlFor="class">Class:</label>
                                        <select className="form-control" value={this.state.classLevel} onChange={this.handleChangeclass}>
                                            <option value="">All</option>
                                            <option value="1">1</option>
                                            <option value="2">2</option>
                                            <option value="3">3</option>
                                        </select>
                                    </div>
                                    <div className="form-group">
                                        <label htmlFor="section">Section:</label>
                                        <select className="form-control" value={this.state.section} onChange={this.handleChangesection}>
                                            <option value="">All</option>
                                            <option value="A">A</option>
                                            <option value="B">B</option>
                                        </select>
                                    </div>
                                </div>
                                <div className="button-container">
                                    <button type="submit" value="Submit" className="btn btn-primary">Search friends</button>
                                </div>
                            </form>
                        </div>
                        <div className="shadow">
                            <h1>{friends}</h1>
                            <div className="row">
                                {
                                    items.map(item => this.displayitem(item, true))
                                }
                                {
                                    non_friend_items.map(item => this.displayitem(item, false))
                                }
                            </div>
                            <h1>{teachers}</h1>
                            <div className="row">
                                {
                                    following_teachers.map(item => this.displayitem(item, true))
                                }
                                {
                                    not_following_teachers.map(item => this.displayitem(item, false))
                                }
                            </div>
                        </div>
                    </div>
            );
        }
    }
}
