const upload = document.getElementById('upload');
const icon = document.querySelector('#upload > span');
const form = document.querySelector('#upload > form');
const text = document.querySelector('#upload > h1');

const uploader = f => {
    upload.removeEventListener('dragleave', dragLeave);
    upload.removeEventListener('dragenter', dragEnter);
    upload.removeEventListener('dragover', dragOver);
    upload.removeEventListener('drop', drop);
    form.classList.add('done');
    icon.classList.remove('drag');
    form.classList.remove('drag');

    icon.classList.add('done');
    text.classList.add('done');
    setTimeout(() => {
        form.style.display = 'none';
        text.innerHTML = 'Uploading...';
        icon.innerHTML = 'sync';
        icon.style.animation = 'spin 2s linear infinite';
        icon.style.animationPlayState = 'running';
        text.classList.remove('done');
        icon.classList.remove('done');

        // upload to backend simulated
        const data = new FormData();
        data.append('file', f);
        fetch('/', {
            method: 'POST',
            body: data,
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
        })
        .then(async res => {
            const d = await res.json();
            document.querySelector('#left > img:first-child').src = d.image;
            document.querySelector('#left > img:last-child').src = d.upload;
            document.querySelector('#right > em').innerHTML = d.type;
            document.querySelector('#right > h1').innerHTML = d.species;
            document.querySelector('#right > p').innerHTML = d.description;
            document.querySelector('#first-param > span').innerHTML = d.poisonous ? 'check' : 'close';
            document.querySelector('#second-param > div > span').innerHTML = d.type === 'snake' ? 'sentiment_very_dissatisfied' : 'whatshot';
            document.querySelector('#second-param > span').innerHTML = d.toxic ? 'check' : 'close';
            document.getElementById('first-link').href = d.image;
            document.getElementById('second-link').href = d.article;

            icon.style.opacity = 0;
            text.style.opacity = 0;
            setTimeout(() => {
                icon.style.display = 'none';
                text.style.display = 'none';
                document.getElementById('wrapper').style.opacity = 1;
                upload.style.overflowY = 'auto';
            }, 200);
            const color = [Math.trunc(Math.random() * 255), Math.trunc(Math.random() * 255), Math.trunc(Math.random() * 255)];
            const darker = [color[0] - 50, color[1] - 50, color[2] - 50];
            upload.style.border = `2px solid rgb(${color[0]}, ${color[1]}, ${color[2]})`;
            upload.style.backgroundColor = `rgb(${darker[0]}, ${darker[1]}, ${darker[2]})`;
            upload.style.filter = `drop-shadow(0px 0px 10px rgb(${color[0]}, ${color[1]}, ${color[2]}))`;
        })
        .catch(() => {
            alert('Error uploading file - Incorrect format or other error');
            location.reload();
        });
    }, 500);
};

document.getElementById('input').addEventListener('change', e => {
    if (e.target.files) uploader(e.target.files[0]);
});

let count = 0;

const dragOver = e => {
    e.preventDefault();
};

const dragEnter = e => {
    count++;
    e.preventDefault();
    icon.classList.add('drag');
    form.classList.add('drag');
};

const dragLeave = () => {
    count--;
    if (!count) {
        icon.classList.remove('drag');
        form.classList.remove('drag');
    }
};

const drop = e => {
    e.preventDefault();
    uploader(e.dataTransfer.files[0]);
};

upload.addEventListener('dragover', dragOver);

upload.addEventListener('dragenter', dragEnter);

upload.addEventListener('dragleave', dragLeave);

document.addEventListener('drop', drop);
