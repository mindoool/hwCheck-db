app.controller('AdminController', ['$scope', 'storage', '$mdMedia', '$mdDialog', '$http', '$filter', 'CommonData', function ($scope, storage, $mdMedia, $mdDialog, $http, $filter, CommonData) {

    //문제목록 불러올 때 필터링 기준 - course 기준
    $scope.selectedCourse = null;
    $scope.targetGroup = 0;
    $scope.courseGroupObj = CommonData.getCourseGroupObj();

    //문제목록 불러오는 거
    $scope.datepicker = {
        "date1": new Date(Date.now()-7*24*60*60*1000),
        "date2": new Date(Date.now()+7*24*60*60*1000)
    };

    $scope.getProblemList = function () {
        var params = {
            "date1": $filter('date')(new Date($scope.datepicker.date1), 'yyyy-MM-dd'),
            "date2": $filter('date')(new Date($scope.datepicker.date2), 'yyyy-MM-dd'),
        };
        $http.get(host + "/groups/" + $scope.targetGroup + "/problems", {params: params}, {cache: true})
            .then(function (response) {
                $scope.dateList2 = [];
                $scope.problemGroupList = [];
                $scope.problemList = response.data.data;

                for (var i = 0; i < $scope.problemList.length; i++) {
                    if ($scope.dateList2.indexOf($scope.problemList[i].date) < 0) {
                        $scope.dateList2.push($scope.problemList[i].date);
                    }
                }

                //for (var i = 0; i < $scope.problemList.length; i++) {
                //    var date = $scope.problemList[i].date;
                //    var group = $scope.userGroupList[i].group;
                //
                //    if (typeof $scope.groupObj[group.id]=="undefined") {
                //        if (typeof $scope.courseObj[course.id]=="undefined") {
                //            $scope.courseObj={};
                //            course.users = [user];
                //            $scope.courseObj[course.id] = course;
                //            console.log('1')
                //        } else {
                //            $scope.courseObj[course.id].users.push(user);
                //            console.log('2')
                //        }
                //        group.courses = [$scope.courseObj];
                //        $scope.groupObj[group.id] = group;
                //        console.log(group);
                //    } else {
                //        if (typeof $scope.courseObj[course.id]=="undefined") {
                //            course.users = [user];
                //            $scope.courseObj[course.id] = course;
                //            console.log('3')
                //        } else {
                //            $scope.courseObj[course.id].users.push(user);
                //            console.log('4')
                //        }
                //        //$scope.courseObj[course.id].groups.push($scope.groupObj);
                //        console.log(group);
                //    }
                //}

                for (var i = 0; i < $scope.problemList.length; i++) {
                    if ($scope.problemGroupList.indexOf($scope.problemList[i].group.name) < 0) {
                        $scope.problemGroupList.push($scope.problemList[i].group.name);
                    }
                }
            });
    };

    //Homework Table에서 과제 가져오기
    $scope.getHwList = function () {
        var params = {
            "date1": $filter('date')(new Date($scope.datepicker.date1), 'yyyy-MM-dd'),
            "date2": $filter('date')(new Date($scope.datepicker.date2), 'yyyy-MM-dd'),
        };
        $http.get(host + "/groups/" + $scope.targetGroup + "/homeworks", {params: params}, {cache: true})
            .then(function (response) {
                $scope.homeworkObj = response.data.data;
            });
    };
    $scope.getHwList();

    //과제를 출제하기 위해 호출하는 함수
    $scope.giveHw = function (hw) {
        $mdDialog.show({
            controller: HwFormatController,
            templateUrl: 'templates/hw-format.html',
            scope: $scope,
            preserveScope: true,
            parent: angular.element(document.body),
            targetEvent: hw,
            clickOutsideToClose: true,
            fullscreen: true
        })
    };

    function HwFormatController($scope, $mdDialog) {
        $scope.hide = function () {
            $mdDialog.hide();
        };
        $scope.cancel = function () {
            $mdDialog.cancel();
        };
        $scope.answer = function (answer) {
            $mdDialog.hide(answer);
        };


        $scope.items = [];

        $scope.fileContent = null;

        $scope.giveHwSubmit = function () {
            var content = {
                content: $scope.fileContent
            };
            console.log($scope.fileContent);
            $http.post(host + '/problems', content)
                .then(function (response) {
                    $scope.hide();
                    console.log(response)
                })
        };

        //변화감지하는 함수
        //$scope.$watch(function() {
        //    return $scope.fileContent;
        //}, function(newVal, oldVal) {
        //   console.log(newVal);
        //});
    }


    //결과 확인을 누르면 개별 결과를 볼 수 있는 함수
    $scope.getResult = function (hw, homework) {
        console.log(homework);
        $mdDialog.show({
            controller: HwResultController,
            templateUrl: 'templates/hw-result.html',
            parent: angular.element(document.body),
            targetEvent: hw,
            clickOutsideToClose: true,
            fullscreen: true,
            locals: {
                homework: homework
            }
        })
    };

    function HwResultController($scope, $mdDialog, homework) {
        $scope.hide = function () {
            $mdDialog.hide();
        };
        $scope.cancel = function () {
            $mdDialog.cancel();
        };
        $scope.answer = function (answer) {
            $mdDialog.hide(answer);
        };

        $scope.currentHomework = homework;

        //서버로 부터 개별과제 받아오는 http.get이 추가되어야 함
        var params = {
            "homeworkId": homework.id
        };
        $http.get(host + "/users-answers", {params: params})
            .then(function (response) {
                console.log(response);
                $scope.userAnswerList = response.data.data;
            });
    }

}]);