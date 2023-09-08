const promptForm = document.getElementById("prompt-form");
const submitButton = document.getElementById("submit-button");
const questionButton = document.getElementById("question-button");
const messagesContainer = document.getElementById("messages-container");
const indiceButton = document.getElementById("indice-button");
const descriptionButton = document.getElementById("description-button");
const appendHumanMessage = (message) => {
  const humanMessageElement = document.createElement("div");
  humanMessageElement.classList.add("message", "message-human");
  humanMessageElement.innerHTML = message;
  messagesContainer.appendChild(humanMessageElement);
};

const appendAIMessage = async (messagePromise) => {
  // Add a loader to the interface
  const loaderElement = document.createElement("div");
  loaderElement.classList.add("message");
  loaderElement.innerHTML =
    "<div class='loader'><div></div><div></div><div></div>";
  messagesContainer.appendChild(loaderElement);

  // Await the answer from the server
  const messageToAppend = await messagePromise();

  // Replace the loader with the answer
  loaderElement.classList.remove("loader");
  loaderElement.innerHTML = messageToAppend;
};


const appendImage = async (imagePromise) => {
  const imageToAppend = await imagePromise();

  // Check if the message is an image URL
  if (isImageURL(imageToAppend)) {
    // Create an image element and set its source
    const imageElement = document.createElement("img");
    imageElement.src = imageToAppend;

    // Append the image to the messages container
    messagesContainer.appendChild(imageElement);
  } else {
    // If it's not an image URL, create a regular message element
    const messageElement = document.createElement("div");
    messageElement.classList.add("message");
    messageElement.innerHTML = imageToAppend;

    // Append the message to the messages container
    messagesContainer.appendChild(messageElement);
  }
};

// Function to check if a string is a valid image URL
const isImageURL = (url) => {
  const imageExtensions = [".jpg", ".jpeg", ".png", ".gif", ".bmp"];
  return imageExtensions.some((ext) => url.toLowerCase().endsWith(ext));
};

const handlePrompt = async (event) => {
  event.preventDefault();
  // Parse form data in a structured object
  const data = new FormData(event.target);
  promptForm.reset();

  let url = "/prompt";
  if (questionButton.dataset.question !== undefined) {
    url = "/answer";
    data.append("question", questionButton.dataset.question);
    delete questionButton.dataset.question;
    questionButton.classList.remove("hidden");
    submitButton.innerHTML = "Message";
  }

  appendHumanMessage(data.get("prompt"));

  await appendAIMessage(async () => {
    const response = await fetch(url, {
      method: "POST",
      body: data,
    });
    const result = await response.json();
    return result.answer;
  });
};

promptForm.addEventListener("submit", handlePrompt);

const handleQuestionClick = async (event) => {
  appendAIMessage(async () => {
    const response = await fetch("/question", {
      method: "GET",
    });
    const result = await response.json();
    const question = result.answer;

    questionButton.dataset.question = question;
    questionButton.classList.add("hidden");
    submitButton.innerHTML = "Répondre à la question";
    return question;
  });
};

questionButton.addEventListener("click", handleQuestionClick);


const handleIndiceClick = async () => {
  if (questionButton.dataset.question !== undefined) {
    appendAIMessage(async () => {
      const response = await fetch("/indice", {
        method: "POST",
        body: JSON.stringify({ question: questionButton.dataset.question }),
        "Content-Type": "text/plain"
      });
      const result = await response.json();
      const indice = result.answer;

      return indice;
    })
  };
  // else{

  // }
};

indiceButton.addEventListener("click", handleIndiceClick);

const handleDescriptionClick = async (event) => {
  // Utilisation de fetch pour obtenir l'URL de l'image depuis le serveur
  const response = await fetch("/image", {
    method: "GET",
  });

  // Vérifiez si la réponse du serveur est correcte (statut 200 OK)
  if (response.status === 200) {
    // Obtenez l'URL de l'image à partir de la réponse JSON (ajustez si nécessaire)
    const imageDescription = await response.json();
    const imageUrl = imageDescription.url; // Suppose que l'URL de l'image est stockée dans une propriété "url"

    // Utilisation de la fonction appendImage pour ajouter l'image au conteneur de messages
    appendImage(() => imageUrl);
  } else {
    // Gérer les erreurs si la demande échoue
    appendHumanMessage("Échec de la récupération de l'image.");
  }
};

descriptionButton.addEventListener("click", handleDescriptionClick);
