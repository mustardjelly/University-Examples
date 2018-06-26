function expand(input) {
	try {
		input = input.value.toString();
	} catch(e) {
		input = "msg1Contents";
	}
	if (input == "msg2Contents"){
		document.getElementById("titleToChange").innerHTML = "Some more feedback";
	}
	msg = document.getElementById(input);
    if (msg.style.display == "none") {
    	msg.style.display = "";
    } else {
    	msg.style.display = "none";
    }	
}

function test() {
	alert("Hello 123");
}

function hideAll() {
	var msgs = ["msg1Contents", "msg2Contents", "reply1", "reply2"];
	for (i = 0; i < msgs.length; i++) {
		msg = document.getElementById(msgs[i]);
		if (msg.style.display == "") {
			msg.style.display = "none";
		}	
	}
}

function defaultLoad() {
	hideAll();
	expand();
}

function addComment() {
	if (changeDiv()) {
		replyTab = document.getElementById("reply1");
		replyTab.style.display = "";
	}
}

function changeDiv(){
	inText = document.getElementById("replyMsg1").value;
	document.getElementById("replyMsg1").value = "";
	if (inText) {
		destination = document.getElementById("fb1");
		destination.innerHTML = inText;
		return true;
	}
}

var replyInput = document.getElementById("replyMsg1");
document.onload(replyInput.addEventListener("keydown", function (e) {
		alert(e);
		if (e.keyCode === 13) {
			changeDiv();
		}
	}
)
)