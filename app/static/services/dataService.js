app.service("dataService", function($http){

    this.getInvoices = function(callback){
        $http.get("/api/invoices").
            then(callback);
    };

    this.deleteInvoice = function(invoice){
        console.log("Deleted from db " + JSON.stringify(invoice));
    };
});
