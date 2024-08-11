def page() -> str:
    page = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cicero</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/htmx/1.9.10/htmx.min.js"></script>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        form {
            display: flex;
            flex-direction: column;
            gap: 10px;
            margin-bottom: 30px;
        }
        textarea {
            height: 100px;
        }
        .result {
            margin-top: 10px;
            padding: 10px;
            border: 1px solid #ccc;
            background-color: #f0f0f0;
        }
        .loading {
            display: none;
            color: #666;
            font-style: italic;
        }
    </style>
</head>
<body>
    <h1>Cicero API</h1>

    <h2>Query</h2>
    <form id="queryForm" data-endpoint="/api/query">
        <label for="queryMessage">Message:</label>
        <textarea id="queryMessage" name="message" required></textarea>
        <button type="submit">Submit Query</button>
    </form>
    <div id="queryLoading" class="loading">Sending query request...</div>
    <div id="queryResult" class="result"></div>

    <h2>Ingest</h2>
    <form id="ingestForm" data-endpoint="/api/ingest">
        <label for="ingestMessage">Message:</label>
        <textarea id="ingestMessage" name="message" required></textarea>
        <button type="submit">Submit Ingest</button>
    </form>
    <div id="ingestLoading" class="loading">Sending ingest request...</div>
    <div id="ingestResult" class="result"></div>

    <h2>Ingest Wiki</h2>
    <form id="ingestWikiForm" data-endpoint="/api/ingest-wiki">
        <label for="ingestWikiMessage">Message:</label>
        <textarea id="ingestWikiMessage" name="message" required></textarea>
        <button type="submit">Submit Ingest Wiki</button>
    </form>
    <div id="ingestWikiLoading" class="loading">Sending ingest-wiki request...</div>
    <div id="ingestWikiResult" class="result"></div>

    <script>
        const baseUrl = 'https://cicero.darley.dev';

        function setupForm(formId) {
            const form = document.getElementById(formId);
            const result = document.getElementById(`${formId.replace('Form', 'Result')}`);
            const loading = document.getElementById(`${formId.replace('Form', 'Loading')}`);
            const endpoint = form.dataset.endpoint;

            form.addEventListener('submit', async (e) => {
                e.preventDefault();
                const message = form.querySelector('textarea').value;
                loading.style.display = 'block';
                result.innerHTML = '';

                try {
                    const response = await fetch(`${baseUrl}${endpoint}`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'text/plain',
                        },
                        body: message,
                    });

                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }

                    const data = await response.text();
                    result.innerHTML = `<h3>Response:</h3><pre>${data}</pre>`;
                } catch (error) {
                    result.innerHTML = `<h3>Error:</h3><p>${error.message}</p>`;
                } finally {
                    loading.style.display = 'none';
                }
            });
        }

        setupForm('queryForm');
        setupForm('ingestForm');
        setupForm('ingestWikiForm');
    </script>
</body>
</html>
"""
    return page