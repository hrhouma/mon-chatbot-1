# partie 02 - Intégration avancée de ChatGPT

------------------
# 1. Configuration de l'API OpenAI
------------------

## 1.1. Installez la bibliothèque OpenAI :

```bash
pip install openai
```

## 1.2. Dans `chatbot_project/settings.py`, ajoutez votre clé API OpenAI :

```python
import os

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', 'votre-clé-api-ici')
```

------------------
# 2. Modification de la vue Django
------------------

Modifiez `chatbot_app/views.py` pour intégrer l'API OpenAI :

```python
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from openai import OpenAI
import json

ai_client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

@csrf_exempt
def chatbot_response(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data['message']
        messages = [
            {"role": "system", "content": "Vous êtes un assistant IA utile et amical."},
            {"role": "user", "content": user_message},
        ]
        chat_completion = ai_client.chat.completions.create(
            messages=messages,
            model="gpt-3.5-turbo",
            temperature=0.7,
            max_tokens=150
        )
        bot_response = chat_completion.choices[0].message.content
        return JsonResponse({'message': bot_response})
    else:
        return JsonResponse({'error': 'Requête invalide'}, status=400)
```

------------------
# 3. Amélioration du frontend React
------------------

Modifiez `chatbot_frontend/src/Chatbot.js` pour gérer l'historique des conversations :

```javascript
import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Chatbot = () => {
    const [messages, setMessages] = useState([]);
    const [userInput, setUserInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    const sendMessage = async () => {
        if (!userInput.trim()) return;
        setIsLoading(true);
        const newMessages = [...messages, { sender: 'user', text: userInput }];
        setMessages(newMessages);
        setUserInput('');

        try {
            const response = await axios.post('http://127.0.0.1:8000/api/chatbot/', { message: userInput });
            setMessages([...newMessages, { sender: 'bot', text: response.data.message }]);
        } catch (error) {
            console.error(error);
        } finally {
            setIsLoading(false);
        }
    };

    useEffect(() => {
        const chatContainer = document.getElementById('chat-container');
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }, [messages]);

    return (
        <div className="chatbot-container">
            <div id="chat-container" className="chat-messages">
                {messages.map((msg, index) => (
                    <div key={index} className={`message ${msg.sender}`}>
                        {msg.text}
                    </div>
                ))}
                {isLoading && <div className="message bot">En train de répondre...</div>}
            </div>
            <div className="chat-input">
                <input
                    type="text"
                    value={userInput}
                    onChange={(e) => setUserInput(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
                    placeholder="Tapez votre message ici..."
                />
                <button onClick={sendMessage} disabled={isLoading}>Envoyer</button>
            </div>
        </div>
    );
};

export default Chatbot;
```

------------------
# 4. Ajout de styles CSS
------------------

Créez un fichier `chatbot_frontend/src/Chatbot.css` :

```css
.chatbot-container {
    max-width: 500px;
    margin: 0 auto;
    border: 1px solid #ddd;
    border-radius: 8px;
    overflow: hidden;
}

.chat-messages {
    height: 400px;
    overflow-y: auto;
    padding: 20px;
    background-color: #f9f9f9;
}

.message {
    margin-bottom: 10px;
    padding: 10px;
    border-radius: 5px;
}

.user {
    background-color: #e6f2ff;
    text-align: right;
}

.bot {
    background-color: #f0f0f0;
}

.chat-input {
    display: flex;
    padding: 10px;
    background-color: #fff;
}

.chat-input input {
    flex-grow: 1;
    padding: 5px;
    border: 1px solid #ddd;
    border-radius: 4px;
}

.chat-input button {
    margin-left: 10px;
    padding: 5px 15px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

.chat-input button:disabled {
    background-color: #cccccc;
}
```

Importez ce fichier CSS dans `Chatbot.js` :

```javascript
import './Chatbot.css';
```




-------------------------
# Annexe 
-------------------------


# Classes, Fichiers et Composants (Exhaustif)

Voici le contenu **complet et détaillé** de chaque fichier que vous avez mentionné, avec des explications pédagogiques pour les étudiants débutants.

---
# **1. App.js (React - Composant Principal)**
---

Le composant `App.js` est le point d'entrée principal de l'application React. Il inclut le composant `Chatbot` que nous avons créé séparément.

```javascript
import React from 'react';
import Chatbot from './Chatbot'; // Importation du composant Chatbot

function App() {
    return (
        <div className="App">
            {/* Ajout du composant Chatbot dans la structure de l'application */}
            <Chatbot />
        </div>
    );
}

export default App;
```

- **Explication :**
  - La fonction `App` retourne un composant React (`<Chatbot />`) encapsulé dans une `div`.
  - La classe CSS `"App"` peut être stylisée dans un fichier séparé (exemple : `App.css`).

---
# **2. Chatbot.js (React - Interface du Chatbot)**
---

Ce composant gère :
- Les messages échangés entre l'utilisateur et le bot.
- La logique d'envoi des messages via une API Django.

```javascript
import React, { useState } from 'react';
import axios from 'axios'; // Axios pour effectuer des requêtes HTTP

const Chatbot = () => {
    const [messages, setMessages] = useState([]); // Historique des messages
    const [userInput, setUserInput] = useState(''); // Saisie de l'utilisateur

    const sendMessage = async () => {
        if (!userInput.trim()) return; // Ignore les saisies vides

        // Ajoute le message de l'utilisateur à l'historique
        const newMessages = [...messages, { sender: 'user', text: userInput }];
        setMessages(newMessages);
        setUserInput(''); // Réinitialise la saisie

        try {
            // Envoi du message à l'API Django
            const response = await axios.post('http://127.0.0.1:8000/api/chatbot/', { message: userInput });
            // Ajoute la réponse du bot à l'historique
            setMessages([...newMessages, { sender: 'bot', text: response.data.message }]);
        } catch (error) {
            console.error(error); // Affiche les erreurs éventuelles
        }
    };

    return (
        <div>
            <h1>Chatbot</h1>
            <div>
                {/* Affiche chaque message */}
                {messages.map((msg, index) => (
                    <p key={index} className={msg.sender}>
                        {msg.sender === 'user' ? 'Vous : ' : 'Bot : '}
                        {msg.text}
                    </p>
                ))}
            </div>
            <input
                type="text"
                value={userInput} // Liaison avec l'état userInput
                onChange={(e) => setUserInput(e.target.value)} // Mise à jour de la saisie utilisateur
                onKeyPress={(e) => e.key === 'Enter' && sendMessage()} // Envoi au "Enter"
            />
            <button onClick={sendMessage}>Envoyer</button> {/* Envoi via bouton */}
        </div>
    );
};

export default Chatbot;
```

- **Explication des parties principales :**
  - **useState** : Gestion des états `messages` (historique) et `userInput` (saisie utilisateur).
  - **axios** : Requête POST à l'API Django pour obtenir la réponse du chatbot.
  - **UI** : Affiche les messages sous forme de paragraphes (`<p>`).

---
# **3. views.py (Django - Logique de l'API)**
---

Cette vue Django reçoit les messages de l'utilisateur via une requête POST, et retourne une réponse JSON simulée.

```python
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt  # Désactivation de la protection CSRF pour tester plus facilement les requêtes
def chatbot_response(request):
    if request.method == 'POST':  # Vérifie si la requête est bien un POST
        data = json.loads(request.body)  # Charge le corps de la requête JSON
        user_message = data.get('message', '')  # Récupère le message utilisateur
        response = f"Vous avez dit : {user_message}"  # Génère une réponse simple
        return JsonResponse({'message': response})  # Retourne la réponse sous forme JSON
    return JsonResponse({'error': 'Requête invalide'}, status=400)
```

- **Explication des parties :**
  - `csrf_exempt` : Utilisé pour désactiver temporairement la vérification CSRF (utile pour les tests locaux).
  - `JsonResponse` : Retourne une réponse en JSON lisible par le frontend.
  - `POST` : Traite uniquement les requêtes POST.

---
# **4. settings.py (Django - Configuration)**
---

Modifiez le fichier de configuration ajusté pour activer **corsheaders** et l’application `chatbot_app`.

```python
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",  # Middleware pour autoriser les requêtes cross-origin
    "chatbot_app",  # Notre application
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",  # Ajout du middleware CORS
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # Autorise les requêtes venant du frontend React
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",  # Base de données SQLite
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
```

---
# **5. urls.py (Django - Routage)**
---

Ce fichier définit les chemins d’accès pour les vues Django.

```python
from django.contrib import admin
from django.urls import path
from chatbot_app.views import chatbot_response  # Import de la vue

urlpatterns = [
    path("admin/", admin.site.urls),  # Page d'administration Django
    path("api/chatbot/", chatbot_response, name="chatbot_response"),  # API pour le chatbot
]
```



- **Explication :**
  - `path("api/chatbot/")` : Définit le point d'accès pour le chatbot, accessible via `/api/chatbot/`.

---

# **Lancement du projet**

1. **Démarrer Django :**
   ```bash
   set OPENAI_API_KEY=sk-proj-7j3JXXXXXXXXXXXXXXgIjdAqT2XXXXXXXXXXXXX
   python manage.py runserver
   ```

2. **Démarrer React :**
   ```bash
   npm start
   ```

![image](https://github.com/user-attachments/assets/eb536c19-6eb4-4b16-8704-f6688803f5d1)


3. **Tester l’application :**
   - Accédez au frontend via [http://localhost:3000](http://localhost:3000).
   - Envoyez un message pour voir la réponse générée par le backend Django.



