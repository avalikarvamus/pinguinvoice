app.controller("pinguController", function($scope, dataService){
    console.log("Controller is alive");

    service.getInvoices(function (response) {
        $scope.invoices = response.data;
        console.log("Loading invoices");
    });

    $scope.edit = function(){
        $scope.editing = !$scope.editing;
        console.log("Edit invoice");
    };

    $scope.deleteInvoice = function(invoice, index){
        $scope.invoices.splice(index, 1);
        service.deleteInvoice(invoice);
        console.log("Deleted from runtime " + index);
    };

    $scope.saveInvoice = function(invoice, index){
        console.log(JSON.stringify(invoice) + " saved.");
    };

    $scope.addInvoice = function(){
        var newInvoice = {name: "New invoice"};
        $scope.invoices.push(newInvoice);
        console.log("Invoice " + JSON.stringify(newInvoice) + " added.");
    };

});
