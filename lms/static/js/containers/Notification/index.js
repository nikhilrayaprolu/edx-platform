import React from 'react';
import { StreamApp, NotificationDropdown} from 'react-activity-feed';
import ReactDOM from 'react-dom';
import {BrowserRouter} from "react-router-dom/";
import '../../scss/index.scss';
class Notification extends React.Component {
  render () {
    console.log(window.apiKey);
    return (
      <StreamApp
        apiKey= {window.apiKey}
        appId= {window.appId}
        token= {window.USER_TOKEN}
      >
        <NotificationDropdown notify/>
      </StreamApp>

    )
  }
}
export default Notification;
ReactDOM.render(
      <Notification />
    ,
      document.getElementById('notification-app'),
    );

