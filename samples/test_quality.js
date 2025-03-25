// This is a poorly written function with multiple issues
function calc(a,b,x) {
    var tmp = 0;
    if(x=="add"){
        tmp=a+b
    }
    if(x=="subtract"){
        tmp=a-b
    }
    if(x=="multiply"){
        tmp=a*b
    }
    if(x=="divide"){
        tmp=a/b
    }
    return tmp;
}

// Bad variable names and no error handling
function getData(url,cb) {
    var d;
    fetch(url).then(function(r) {
        d = r.json();
        cb(d);
    })
}

// Long function with repeated code
function processUserData(userData) {
    let final = [];
    for(let i = 0; i < userData.length; i++) {
        if(userData[i].type === 'admin') {
            final.push({
                name: userData[i].name,
                email: userData[i].email,
                access: 'full',
                canEdit: true,
                canDelete: true,
                canInvite: true
            });
        }
        if(userData[i].type === 'editor') {
            final.push({
                name: userData[i].name,
                email: userData[i].email,
                access: 'partial',
                canEdit: true,
                canDelete: false,
                canInvite: false
            });
        }
        if(userData[i].type === 'viewer') {
            final.push({
                name: userData[i].name,
                email: userData[i].email,
                access: 'readonly',
                canEdit: false,
                canDelete: false,
                canInvite: false
            });
        }
    }
    return final;
} 