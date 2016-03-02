app.service('CommonData', ['$http', function ($http) {
    var rootCourseList = {};


    this.setGroupObj = function (groupObj) {
        rootGroupObj = groupObj;
    };

    this.getGroupObj = function () {
        return rootGroupObj;
    };

    this.setCourseList = function (courseList) {
        rootCourseList = courseList;
    };

    var courseGroupObj = {};
    var responseList = [];
    var groupList =[];
    var courseList = [];

    $http.get(host + "/courses")
        .then(function(response) {
            responseList = response.data.data;
            for (var i = 0; i < responseList.length; i++) {
                var course = responseList[i];
                courseList.push(course);
                var groups = responseList[i].groups;
                for (var j = 0; j < groups.length; j++) {
                    groups[j]['course']=course
                    groupList.push(groups[j]);

                    if (typeof courseGroupObj[course.id] == "undefined") {
                        course.groups = [groups[j]];
                        courseGroupObj[course.id] = course;
                    } else {
                        courseGroupObj[course.id].groups.push(groups[j]);
                    }
                }

            }
            console.log(courseGroupObj);
        });

    this.getCourseGroupObj = function () {
        return courseGroupObj
    };

    this.getGroupList = function () {
        console.log(groupList);
        return groupList
    }

    this.getCourseList = function () {
        return courseList
    }
}]);