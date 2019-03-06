import React from 'react';
import { StreamApp, NotificationDropdown, FlatFeed, LikeButton, Activity, CommentList, CommentField, StatusUpdateForm} from 'react-activity-feed';
import 'react-activity-feed/dist/index.css';
import Home from '../../components/Home'
import Feed from '../../components/Feed'
import Group from '../../components/Group'
import {Route, Switch} from "react-router-dom";
import UnApprovedGroup from "../../components/UnApprovedGroup";

class App extends React.Component {
  render () {
    const text = 'Django + React + Webpack + Babel = Awesome App';
    console.log(window.apiKey)
    return (
      <StreamApp
        apiKey= {window.apiKey}
        appId= {window.appId}
        token= {window.USER_TOKEN}
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
