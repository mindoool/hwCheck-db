app.directive('fileReader', function () {
    return {
        scope: {
            fileReader: "="
        },
        link: function (scope, element) {
            $(element).on('change', function (changeEvent) {
                var files = changeEvent.target.files;
                if (files.length) {
                    var r = new FileReader();
                    r.onload = function (e) {
                        var array = [];
                        var contents = e.target.result;
                        var lines = contents.split(/[\r\n]+/g);
                        var headers = lines[0].split(",");
                        array.push({"headers":headers});

                        for(var i = 1; i < lines.length-1; i++) {
                            array.push({"data":lines[i].split(",")});
                            }


                        scope.$apply(function () {
                            scope.fileReader = array;
                        });
                    };

                    r.readAsText(files[0]);

            };
        })
    }}
});