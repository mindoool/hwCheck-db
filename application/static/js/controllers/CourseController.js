app.controller('CourseController', ['$scope', 'storage', '$mdMedia', '$mdDialog', '$http', '$filter','CommonData', function ($scope, storage, $mdMedia, $mdDialog, $http, $filter, CommonData) {
    //과정 생성하는 함수
    $scope.courseList = CommonData.getCourseList();

    //$scope.getCourse = function() {
    //    $http.get(host + "/courses")
    //        .then(function (response) {
    //            console.log(response);
    //            $scope.courseList = response.data.data;
    //        });
    //};
    //
    //$scope.getCourse();

    $scope.createCourseDialog = function (course) {
        $mdDialog.show({
            controller: CourseDialogController,
            templateUrl: 'templates/create-course.html',
            parent: angular.element(document.body),
            targetEvent: course,
            clickOutsideToClose: true,
            fullscreen: true,
            scope:$scope,
            preserveScope : true,
            course: course
        })
    };

    function CourseDialogController($scope, $mdDialog, course) {
        $scope.hide = function () {
            $mdDialog.hide();
        };
        $scope.cancel = function () {
            $mdDialog.cancel();
        };
        $scope.answer = function (answer) {
            $mdDialog.hide(answer);
        };

        //서버로 부터 개별과제 받아오는 http.get이 추가되어야 함
        $scope.course = {
            name:""
        };

        $scope.currentCourse = {
            name:course.name
        };

        $scope.createCourse = function () {
            var courseData = {
                name: $scope.course.name
            };
            $http.post(host+'/courses', courseData)
                .then(function(response) {
                    console.log(response);
                    $scope.getCourse();

                    $scope.hide();
                })
        };

        $scope.editCourse = function () {
            var courseData = {
                name: $scope.currentCourse.name
            };
            $http.put(host+"/courses/"+course.id, courseData)
                .then(function(response) {
                    console.log(response);
                    $scope.getCourse();
                    $scope.cancel();
                });
        }
    }


    //과정 수정하는 함수
    $scope.editCourseDialog = function (event, course) {
        $mdDialog.show({
            controller: CourseDialogController,
            templateUrl: 'templates/edit-course.html',
            parent: angular.element(document.body),
            targetEvent: event,
            clickOutsideToClose: true,
            fullscreen: true,
            scope:$scope,
            preserveScope : true,
            locals: {
                course: course
            }
        })
    };


    //과정 삭제
    $scope.deleteCourse = function(id) {
        console.log('delete');
        $http.delete(host+"/courses/"+id)
            .then(function (response) {
                console.log(response);
                $scope.getCourse()
            });
    };


}]);