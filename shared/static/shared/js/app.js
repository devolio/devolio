(function(){
    "use strict";
    let upvotes = document.querySelectorAll('.upvote');
    let CSRFToken = document.cookie.replace(/(?:(?:^|.*;\s*)csrftoken\s*\=\s*([^;]*).*$)|^.*$/, "$1");
    let post = (data) => {
        return fetch('/response_reaction', {
                    method: 'POST',
                    credentials: 'same-origin',
                    headers: new Headers({'X-CSRFToken': CSRFToken}),
                    body: JSON.stringify(data)
                });
    };

    let handleUpvotes = (data) => {
        data = JSON.parse(data);
        switch (data.action) {
            case 'dec':
                document.getElementById('rid-count-' + data.rid).innerText--;
                break;
            default:
                document.getElementById('rid-count-' + data.rid).innerText++;
        }

    }

    let upvoteResp = (res) => {
        if (res.ok) {
            res.text().then(handleUpvotes);
        } else {
            console.log(res.statusText);
        }
    };

    for (let upvote of upvotes) {
        upvote.onclick = () => {
            let rid = upvote.dataset.rid
            post({rid: rid}).then(upvoteResp);
        }
    }
})();