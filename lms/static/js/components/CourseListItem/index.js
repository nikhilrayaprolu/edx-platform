import React from 'react';
export default class CoursesListItem extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
        apiFetchActive: false,
        courseData: this.props.courseData,
    }

    //this.redirect = this.redirect.bind(this);
  }
    redirect() {
      //this.props.history.push('courses/'+this.state.courseData.course_id)
    }
    render() {
    console.log(this.state.courseData)
    return this.state.courseData && (
      <React.Fragment>
          <div className="card  mt-2">
              <div className="row no-gutters">
                  <div className="col-md-3">
                      <img src={this.state.courseData.course_details.course_image_url} className="card-img" onError={(e)=>{e.target.onerror = null; e.target.src="https://www.edx.org/sites/default/files/course/image/promoted/edx101.jpg"}} />
                  </div>
                  <div className="col-md-6">
                      <div className="card-body">
                          <h5 className="card-title">{this.state.courseData.course_details.course_name}</h5>
                      </div>
                  </div>
                  <div className="col-md-3">
                      <div className="card-body">
                          <button type="button" className="btn btn-primary button-courses" style={{borderRadius: '10px%'}} onClick={this.redirect}><a style={{textDecorationLine: 'None'}} href={'courses/'+this.state.courseData.course_details.course_id}>{this.props.buttontext}</a></button>
                      </div>
                  </div>
              </div>
          </div>


      </React.Fragment>
    );
  }
}
