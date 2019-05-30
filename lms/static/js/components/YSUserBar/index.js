import React from 'react';
import { humanizeTimestamp } from '../../utils';
import { Dropdown, Link } from 'react-activity-feed';

/**
 * Component is described here.
 *
 * @example ./examples/UserBar.md
 */
export default class UserBar extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            isLoaded: false,
            userid: ""
        };
    }
    componentDidMount() {
        fetch('/youngwall/me')
            .then(res => res.json())
            .then((result) => {
                this.setState({
                    isLoaded: true,
                    userid: result,
                });
            }, (error) => {
                this.setState({
                    isLoaded: true,
                    userid: ""
                })
            });
    }

    render() {
        console.log("testing")

      let timestamp = this.props.activity.time;
      console.log(this.props.activity);
      let username = (this.props.activity.actor.data)? this.props.activity.actor.data.name: this.props.activity.actor;
      let username_id = (this.props.activity.actor.data)? this.props.activity.actor.data.id: this.props.activity.actor.id;
      if(("parent" in this.props) && this.props.parent=="schooldash"){
            username = username.slice(0, 8)

        }
        let time = humanizeTimestamp(timestamp);
        const {isLoaded, userid} = this.state;
        let renderDropDown = null;
        console.log(this.props);
            renderDropDown = (
                <Dropdown>
                    <div>
                        <Link onClick={() => {this.props.onRemoveActivity(this.props.activity.id);}}>Remove</Link>
                    </div>
                </Dropdown>
            );
    return (
      <div className="raf-user-bar">
        <div className="raf-user-bar__details">
            <div id="profileImage">{username[0]}</div>
          <p
            className="raf-user-bar__username"
            onClick={this.props.onClickUser}
          >
              {username}
          </p>
          {this.props.icon !== undefined ? (
            <img src={this.props.icon} alt="icon" />
          ) : null}
          {this.props.subtitle ? (
            <p className="raf-user-bar__subtitle">
              <time
                dateTime={time}
                title={time}
              >
                {this.props.subtitle}
              </time>
            </p>
          ) : null}
        </div>
        <React.Fragment>
            <span className="raf-user-bar__extra">
              <time
                dateTime={time}
                title={time}
              >
                {time}
              </time>
                {renderDropDown}
            </span>
        </React.Fragment>
      </div>
    );
  }
}
