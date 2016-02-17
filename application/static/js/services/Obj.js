app.service('Obj', [function () {
    var rootGroupList = {};
    var rootCourseList = {};

    this.rootCourseList = [];

    this.setGroupObj = function(groupObj) {
        rootGroupObj = groupObj;
    };

    this.getGroupObj = function() {
        return rootGroupObj;
    };

    this.setCourseList = function(courseList) {
        rootCourseList = courseList;
    };

    this.getCourseList = function() {
        return rootCourseList;
    };
}]);