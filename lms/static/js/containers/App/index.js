import React from 'react';
import { StreamApp, NotificationDropdown, FlatFeed, LikeButton, Activity, CommentList, CommentField, StatusUpdateForm} from 'react-activity-feed';
import 'react-activity-feed/dist/index.css';
import Home from '../../components/Home'
import Feed from '../../components/Feed'
import Group from '../../components/Group'
import {Route, Switch} from "react-router-dom";
import UnApprovedGroup from "../../components/UnApprovedGroup";
import ReactDOM from 'react-dom';
import {BrowserRouter} from "react-router-dom/";

class App extends React.Component {
  render () {
    const text = 'Django + React + Webpack + Babel = Awesome App';
    console.log(window.apiKey)
    return (
      <StreamApp
        apiKey= "jkmk5yczhm7d"
        appId= "48329"
        token= "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoidXNlci1vbmUifQ.OT6TSv8GXRm-O7Qx7sFQZ-ScxJxEfzLzJc6znN6ufYY"
      >
        <NotificationDropdown notify/>
        <Switch>
        <Route exact path='/' component={Home}/>
          <Route path='/group/:groupid' component={Group}/>
          <Route path='/unapprovedgroup/:groupid' component={UnApprovedGroup}/>
          <Route path='/:userid' component={Feed}/>

      </Switch>
      </StreamApp>

    )
  }
}
export default App;
ReactDOM.render(
    <BrowserRouter>
      <App />
      </BrowserRouter>,
      document.getElementById('react-app'),
    );

