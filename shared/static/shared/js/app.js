(function(){
    "use strict";
    let print = console.log;
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

    let getReponses = () => {
        // returns all node inside all responses that are not code blocks
        let cleanNode = (node) => {
            // only return non-'code' tags non-parent nodes
            if (node.children.length == 0 && node.tagName != 'CODE') return node;
        }
        let filterResp = (resp) => {
            return [].slice.call(resp.querySelectorAll('*')).filter(cleanNode)
        }
        return [].concat.apply([],
            [].slice.call(document.querySelectorAll('.response-content')).map(filterResp));
    }
    for (let resp of getReponses()) {
        let mentions = resp.innerText.match(/\B@[a-z0-9_-]+/gi);
        if (mentions) {
            for (let m of mentions) {
                let mLink = '<a href="/' + m +'">'+ m + '</a>';
                resp.innerHTML = resp.innerHTML.replace(m, mLink)
            }
        }
    }

})();