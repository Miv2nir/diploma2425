export async function getRequest(url) {
    //moving to async otherwise this will be way too overcomplicated
    try {
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error(`Response status: ${response.status}`);
      }
      const json = await response.json();
      //console.log(json);
      return json;
    } catch (error) {
      console.error(error.message);
      return null;
    }
  }

  export async function postRequest(url,csrftoken) {
    //moving to async otherwise this will be way too overcomplicated
    try {
      const response = await fetch(url,{
        method:"POST",
        headers:{'X-CSRFToken': csrftoken},
        mode: 'same-origin'
      });
      if (!response.ok) {
        throw new Error(`Response status: ${response.status}`);
      }
      //const json = await response.json();
      //console.log(json);
      //return json;
    } catch (error) {
      console.error(error.message);
      return null;
    }
  }