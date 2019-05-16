import React from 'react';
import { StreamApp, NotificationDropdown, FlatFeed, LikeButton, Activity, CommentList, CommentField, StatusUpdateForm} from 'react-activity-feed';
import Home from '../../components/Home'
import Feed from '../../components/Feed'
import Group from '../../components/Group'
import Friends from '../../components/Friends'
import {Route, Switch} from "react-router-dom";
import UnApprovedGroup from "../../components/UnApprovedGroup";
import SchoolFeed from "../../components/School";
import CourseGroup from "../../components/Course";
import SearchUsers from "../../components/searchfilter";
import GroupStats from "../../components/GroupStats";
import Followers from "../../components/Followers";
import ReactDOM from 'react-dom';
import {BrowserRouter} from "react-router-dom/";
import '../../scss/index.scss';

class App extends React.Component {
  render () {
    return (
      <StreamApp
        apiKey= {window.apiKey}
        appId= {window.appId}
        token= {window.USER_TOKEN}
      >
        <NotificationDropdown notify/>
        <Switch>
        <Route exact path='/youngwall/' component={Home}/>
          <Route path='/youngwall/group/:groupid' component={Group}/>
          <Route path='/youngwall/search/users/' component={SearchUsers}/>
          <Route path='/youngwall/unapprovedgroup/:groupid' component={UnApprovedGroup}/>
          <Route path='/youngwall/friends' component={Friends}/>
          <Route path='/youngwall/myfollowers' component={Followers}/>
          <Route path='/youngwall/school/:schoolid' component={SchoolFeed}/>
          <Route path='/youngwall/school' component={SchoolFeed}/>
          <Route path='/courses/:courseid/course_wall/' component={CourseGroup}/>
          <Route path='/youngwall/groupstats' component={GroupStats}/>
          <Route path='/youngwall/:userid' component={Feed}/>

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

