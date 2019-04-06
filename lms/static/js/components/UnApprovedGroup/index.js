import React from 'react';
import {
    FlatFeed,
} from "react-activity-feed";
import UnApprovedPlaceholder from "../unapprovedplaceholder";
import UnApprovedFooter from "../UnApprovedFooter";
import {feedrequest, getCookie} from "../../utils";
const UnMountActivityContext = React.createContext(null);
class UnApprovedGroup extends React.Component {
    constructor(props) {
        super(props);
        console.log("inside unapproved", this.props)
        this.state = {
            unmountedactivities: null,
        };
        this.activityapprove = this.activityapprove.bind(this);
        this.feedgroup = "unapprovedgroup";
        this.feedid = this.props.groupid;

    }
    activityapprove(id, approve, decline){
        var csrftoken = getCookie('csrftoken');
        let params = {
            feed_id: id,
            feed_group: this.props.groupid,
            approve: approve,
            decline: decline
        };
        fetch("/youngwall/approve/",{
            headers: {
                "Content-Type": 'application/json; charset=utf-8',
                'X-CSRFToken': csrftoken
            },
            method: 'post',
            body: JSON.stringify(params),
        })
            .then(res => res.json())
            .then(
                (result) => {
                    console.log('approved successfully')
                },
                (error) => {
                    console.log('approve unsuccessful')
                }
            )
    }

    render () {
        console.log("came into feed");
        let presentvalue = this.state.unmountedactivities;
        console.log(presentvalue);
        return (
            <React.Fragment>
                <FlatFeed
                    feedGroup = {this.feedgroup}
                    userId = {this.feedid}
                    doFeedRequest = {feedrequest}
                    Placeholder = {UnApprovedPlaceholder}
                    Activity={(props) => {
                        console.log(props, presentvalue);
                        return <UnApprovedFooter {...props} presentvalue={presentvalue} activityapprove={this.activityapprove} />
                    }
                    }


                />

            </React.Fragment>

        )
    }
}
export default UnApprovedGroup
