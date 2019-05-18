import React from 'react';
import FollowButton from "../followbutton";
import {handlefollow} from "../../utils";
import {getCookie} from "../../utils";

class GroupStats extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            error: null,
            isLoaded: false,
            courses_following_details: [],
            courses_not_following_details: [],
            global_group_following_details: [],
            global_group_not_following_details: [],
        };
        this.userid = window.userid
    }
    handlefollow(id, type) {
        if(type == 'course') {
            handlefollow(this.userid, id, type);
        } else {
            handlefollow(this.userid, id, 'globalgroup');
        }

    }
    componentWillMount() {
        var csrftoken = getCookie('csrftoken');
        console.log("added csrftoken", csrftoken);
        fetch("/youngwall/groupstatslist", {
        credentials: 'include',
        headers: {
            contentType: 'application/json; charset=utf-8',
            'X-CSRFToken': csrftoken
        },
    })
            .then(res => res.json())
            .then(
                (result) => {
                    this.setState({
                        isLoaded: true,
                        courses_following_details: result.courses_following_details,
                        courses_not_following_details: result.courses_not_following_details,
                        global_group_following_details: result.global_group_following_details,
                        global_group_not_following_details: result.global_group_not_following_details,
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

    displayitem(item, type, follow) {
        console.log(item)
        return (
            <div className="col-md-12 border-bottom" key={item.page_id}>
                <div className="row">
                    <div className="col-md-2">
                        <a>
                            <div id="profileImage">{item.name[0]}</div>
                        </a>
                    </div>
                    <div className="col-md-6">
                        <h4><a href={"/youngwall/" + type + '/'+ item.page_id}>{item.name}</a></h4>
                        <p>{item.description}<br/>
                        </p>
                    </div>
                    <div className="col-md-2">
                        <FollowButton followed={follow} clicked={() => this.handlefollow(item.page_id, type)}/>
                    </div>
                </div>

            </div>
        )
    }

    displaycourseitem(item, type, follow) {
        return (
            <div className="col-md-12 border-bottom" key={item.page_id}>
                <div className="row">
                    <div className="col-md-2">
                        <a>
                            <div id="profileImage">{item.name[0]}</div>
                        </a>
                    </div>
                    <div className="col-md-6">
                        <h4><a href={"/courses/" + item.course_id + '/course_wall/'}>{item.name}</a></h4>
                        <p>{item.description}<br/>
                        </p>
                    </div>
                    <div className="col-md-2">
                        <FollowButton followed={follow} clicked={() => this.handlefollow(item.page_id, type)}/>
                    </div>
                </div>

            </div>
        )
    }
    render () {
        console.log("came into groupstats");
        const { error, isLoaded, courses_following_details,
            courses_not_following_details,
            global_group_following_details,
            global_group_not_following_details} = this.state;
        return (
            <React.Fragment>
                <div id="react-feed">
                <div className="shadow">
                    <h1>Courses</h1>
                    <div className="row">
                        {
                            courses_following_details.map(item => {
                                console.log(item)
                             item.name = item.course_name
                             item.description = item.description
                                return item
                            }).map(item => this.displaycourseitem(item,'course_wall', true))
                        }
                        {
                            courses_not_following_details.map(item => {
                                console.log(item)
                             item.name = item.course_name
                             item.description = item.description
                                return item
                            }).map(item => this.displaycourseitem(item,'course_wall', false))
                        }
                    </div>
                    <h1>Available Global Groups</h1>
                    <div className="row">
                        {
                            global_group_following_details.map(item => this.displayitem(item, 'group', true))
                        }
                        {
                            global_group_not_following_details.map(item => this.displayitem(item, 'group', false))
                        }
                    </div>
                </div>
                    </div>
            </React.Fragment>

        )
    }
}
export default GroupStats
