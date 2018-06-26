// Hides all fields
function hideAll() {
    var mainFields = ["homeMain", "aboutMain", "bookMain", "blurayMain", "commentMain", "registerMain", "purchaseInformation"];
    for (var i = 0; i < mainFields.length; i++){
        document.getElementById(mainFields[i]).style.display = 'none';
    }
}

// Used to display a certain field based on an argument
function showField(id) {
    var title = '';
    hideAll();
    // Set subtitle
    if (id == 'homeMain'){
        title = 'Main Page';
    } else if (id == 'aboutMain'){
        title = 'About';
    } else if (id == 'blurayMain'){
        title = 'Blu-Rays';
    } else if (id == 'bookMain'){
        title = 'Books';
    } else if (id == 'commentMain'){
        title = 'Comments';
    } else if (id == 'registerMain'){
        title = 'Register';
    } else if (id == 'purchaseInformation'){
        title = 'Purchase';
    }
    // Display tab
    document.getElementById('subTitle').innerHTML = title;
    document.getElementById(id).style.display = 'block';
    
    // Blank the search boxes
    if (title == "Blu-Rays") {
        document.getElementById("BRSearch").value = "";
        search("br");
    } else if (title == "Books") {
        document.getElementById("bookSearch").value = "";
        search("book");
    }
} 

// Search/Display book/blu-ray lists
function search(term) {
    // Declare variables
    if (term == 'book'){
        var searchTerm = document.getElementById('bookSearch').value;
        var uri = "http://redsox.uoa.auckland.ac.nz/BC/Open/Service.svc/booksearch?term=" + searchTerm;
    } else {
        var searchTerm = document.getElementById('BRSearch').value;
        var uri = "http://redsox.uoa.auckland.ac.nz/BC/Open/Service.svc/brsearch?term=" + searchTerm;
    }
    var out_line = "<tr class='listHeader'><td class='imgHeader'>Cover</td><td class='titleHeader'>Title</td></tr>";
    var xhr = new XMLHttpRequest();
    // Connect to server to get dynamic list
    xhr.open("GET", uri, true);
    xhr.setRequestHeader("Accept", "application/json");
    xhr.onload = function() {
        var resp = JSON.parse(xhr.responseText);
        for (var i = 0 ; i < resp.length; ++i) {
            if (term == 'book'){
                var img_url = "http://redsox.uoa.auckland.ac.nz/BC/Open/Service.svc/bookimg?id=" + resp[i].Id;
                var buy_url = "http://redsox.uoa.auckland.ac.nz/BC/Closed/Service.svc/bookbuy?id=" + resp[i].Id;
            } else {
                var img_url = "http://redsox.uoa.auckland.ac.nz/BC/Open/Service.svc/brimg?id=" + resp[i].Id;
                var buy_url = "http://redsox.uoa.auckland.ac.nz/BC/Closed/Service.svc/brbuy?id=" + resp[i].Id;
            }
            // Code taken from Mano's Northwind Slides
            if (i & 1 == 1) { //odd row
                out_line += "<tr class='lineOdd' onclick='purchase(\""+buy_url+"\", \""+resp[i].Title+"\")'>";
            } else { //even row
                out_line += "<tr class='lineEven' onclick='purchase(\""+buy_url+"\", \""+resp[i].Title+"\")'>";
            }
            if (term == 'book'){
                var author = resp[i].AuthorInitials + " " + resp[i].AuthorSurname;
                out_line += "<td class='listImages'>" + "<img src=" + img_url +"></url>" + "</td><td class='listTitle'>" + resp[i].Title + "<br><span class='author'>" + author + "</span></td></tr>";
            } else{
                out_line += "<td class='listImages'>" + "<img src=" + img_url +"></url>" + "</td><td class='listTitle'>" + resp[i].Title + "</td></tr>";
            }
        }
        // Output to respective tabs
        if (term == 'book'){
            document.getElementById('bookList').innerHTML = out_line;
        } else {
            document.getElementById('BRList').innerHTML = out_line;
        }
    }
    xhr.send(null);
}

// Provides purchasing functionality
function purchase(buy_url, title) {
    // Declare variable
    var message = "Are you sure you wish to purchase " + title + "?";
    // Confirm purchase
    var canPurchase = confirm(message);
    if (canPurchase){
        document.getElementById('purchaseInformation').innerHTML = '<iframe id="purchasePage" src="'+buy_url+'" style="border:none;"></iframe>';
        showField('purchaseInformation');
    } else {
        alert('Purchase cancelled')
    }
}

// Provides submission functionality for forms
function submit(Id){
    // Declare variables
    var outLine;
    var xhr = new XMLHttpRequest();
    if (Id == 'registration'){
        var name = document.getElementById('registerName').value;
        var password = document.getElementById('registerPassword').value;
        var password2 = document.getElementById('confirmPassword').value;
        var address = document.getElementById('registerAddress').value;
        var myUser = {"Address":address, "Name":name, "Password":password}
        var uri = "http://redsox.uoa.auckland.ac.nz/BC/Open/Service.svc/register";
        // Validation
        if (name == ""){
            alert("You must enter a username");
        } else if (password == ""){
            alert("You must enter a password");
        } else if (password != password2){
            alert('Passwords do not match');
            document.getElementById('registerPassword').value = "";
            document.getElementById('confirmPassword').value = "";
        } else if (address == ""){
            alert('You must enter an address');
        }
        // Do all the things
        else{
            xhr.open("POST", uri, true);
            xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
            xhr.onload = function () {
                var resp = xhr.responseText;
                // Success
                if (resp == '"User registered"'){
                    resp = 'Thanks for registering '+ name +'\nUse this account to purchase products.';
                }
                // Registration information
                alert(resp);
            }
            xhr.send(JSON.stringify(myUser));
        }
    } else if (Id == 'comment') {
        var name = document.getElementById('commentName').value;
        var comment = document.getElementById('commentBox').value;
        var uri = "http://redsox.uoa.auckland.ac.nz/BC/Open/Service.svc/comment?name=" + name;
        // Validate fields for submission
        if (name == ""){
            alert("You must enter a username");
        } else if (comment == ""){
            alert("You must enter a comment");
        }
        // Posting comment to server if validation checks are passed
        else {
            xhr.open("POST", uri, true);
            xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
            xhr.onload = function () {
                document.getElementById('commentName').value = "";
                document.getElementById('commentBox').value = "";
                document.getElementById('commentList').src = document.getElementById('commentList').src;
            }
            xhr.send(JSON.stringify(comment));
        }
    }
    
}

// Clear the registration/comment form
function clearForm(Id) {
    var clear = confirm("Are you sure you wish to clear your form?");
    if (clear) {
        if (Id == 'registration'){
            document.getElementById('registerName').value = "";
            document.getElementById('registerAddress').value = "";
            document.getElementById('registerPassword').value = "";
            document.getElementById('confirmPassword').value = "";
        } else if (Id == 'comment'){
            document.getElementById('commentName').value = "";
            document.getElementById('commentBox').value = "";
            document.getElementById('commentList').src = document.getElementById('commentList').src
        }
    }
}

// Initial Configuration
showField('homeMain');
search('book');
search('br');