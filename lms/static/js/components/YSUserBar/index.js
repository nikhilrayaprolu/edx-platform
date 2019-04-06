import React from 'react';
import { humanizeTimestamp } from '../../utils';

/**
 * Component is described here.
 *
 * @example ./examples/UserBar.md
 */
export default class UserBar extends React.Component {
  render() {
      let timestamp = this.props.activity.time;
      console.log(this.props.activity)
      let username = (this.props.activity.actor.data)? this.props.activity.actor.data.name: this.props.activity.actor;
    let time = humanizeTimestamp(timestamp);
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
            <p className="raf-user-bar__extra">
              <time
                dateTime={time}
                title={time}
              >
                {time}
              </time>
            </p>
        </React.Fragment>
      </div>
    );
  }
}
