import React from 'react';
import FollowButton from "../followbutton";
import {handlefollow} from "../../utils";

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
        this.userid = this.props.userid
    }
    handlefollow(id, type) {
        if(type == 'course') {
            handlefollow(this.userid, id, type);
        } else {
            handlefollow(this.userid, id, 'globalgroup');
        }

    }
    componentDidMount() {

        fetch("/youngwall/groupstatslist")
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
            <div className="col-md-12 border-bottom border-top" key={item.page_id}>
                <div className="row">
                    <div className="col-md-2">
                        <a>
                            <div id="profileImage">{item.name[0]}</div>
                        </a>
                    </div>
                    <div className="col-md-5">
                        <h6><a href={"/" + type + item.page_id}>{item.name}</a></h6>
                        <p>{item.description}<br/>
                        </p>
                    </div>
                    <div className="col-md-2" style={{padding: '0px'}}>
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
                    <div className="section__dash"></div>
                    <h1 className="section__title" style={{fontSize: '1.25rem'}}>{this.props.section_title} </h1>
                    <div className="row">
                        {
                            global_group_following_details.map(item => this.displayitem(item, 'group', true))
                        }
                        {
                            global_group_not_following_details.map(item => this.displayitem(item, 'group', false))
                        }
                    </div>
            </React.Fragment>

        )
    }
}
export default GroupStats
