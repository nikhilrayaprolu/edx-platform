import React from "react";
import {Activity} from "react-activity-feed";
import UserBar from "../YSUserBar";

class UnApprovedFooter extends React.Component {
    constructor(props) {
        super(props);
        console.log("inside footer", this.props)
        this.state = {
            approve: null,
            decline: null
        };
    }
    changefooter(approve, decline) {
        if(approve) {
            this.setState({
                approve: true,
                decline: null,
            })
        } else {
            this.setState({
                approve: null,
                decline: true,
            })
        }

    }
    render() {
        if(this.state.approve) {
            return (
                null
            )

        } else if (this.state.decline) {
            return (
                null
            )

        } else {
            return (
                <React.Fragment>
                    <Activity {...this.props}
                        Header={() => (
                                          <UserBar {...this.props} />
                                      )}

                              Footer={() => (
                                  <div style={{padding: '8px 16px'}}>
                                      <button type="button" className="btn btn-primary" onClick={() => {this.props.activityapprove(this.props.activity.id, true, false);this.changefooter(true, null)}}>Approve</button>
                                      <button type="button" className="btn btn-danger" onClick={() => {this.props.activityapprove(this.props.activity.id, false, true);this.changefooter(null, true)}}>Decline</button>
                                  </div>
                              )}
                    />
                </React.Fragment>
            )

        }

    }

}

export default UnApprovedFooter
