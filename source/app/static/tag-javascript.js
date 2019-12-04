$(document).ready(function() {
  $(window).keydown(function(event){
    if(event.keyCode == 13) {
      event.preventDefault();
      return false;
    }
  });

  let collectionOfTags = document.querySelector('.collection-of-tags');
  let collectionOfTagsInput = document.querySelector('#tag-input');
  let hiddenTagField = document.querySelector('#hidden-tag-list-value');
  let tags = [];

  set_value();

  function set_value() {
    if (hiddenTagField.value !== ''){
      tags = hiddenTagField.value.split(',');
      addTags();
    }
  }

  function createTag(label){
    let div = document.createElement('div');
    div.setAttribute('class', 'tag-div');

    let span = document.createElement('span');
    span.innerHTML = label;

    let icon = document.createElement('i');
    icon.setAttribute('class', "fas fa-times-circle");
    icon.setAttribute('id', "close-icon");
    icon.setAttribute('data-item', label)

    div.appendChild(span);
    div.appendChild(icon);
    return div;
  }

  function reset() {
    document.querySelectorAll('.tag-div').forEach(function(t){
      t.parentElement.removeChild(t);
    })
  }

  function addTags() {
    reset();
    tags.forEach(function(tag){
      let new_tag = createTag(tag);
      collectionOfTags.appendChild(new_tag);
    })
    setHiddenField();
  };

  collectionOfTagsInput.addEventListener('keyup', function(e){
    if ( e.key === 'Enter'){
      let new_tags = collectionOfTagsInput.value.split(" ")
      console.log(new_tags);
      new_tags.forEach(function (item){
        tags.push(item);
      })
      addTags();
      collectionOfTagsInput.value = '';
    }
  });

  document.addEventListener('click', function(e){
    if (e.target.tagName === "I"){
      var value = e.target.getAttribute('data-item');
      let index = tags.indexOf(value);
      tags = [...tags.slice(0,index),...tags.slice(index+1)];
      addTags();
    }
  });

  function setHiddenField(){
    hiddenTagField.value = tags.join(', ');
  }
});
