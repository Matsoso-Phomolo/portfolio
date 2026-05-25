# Stripe Backend

Run this backend from the `backend` folder before testing Stripe buttons from the local `index.html` file:

```bash
pip install -r requirements.txt
uvicorn main:app --host 127.0.0.1 --port 8000
```

Create a local `.env` file with:

```env
STRIPE_SECRET_KEY=sk_test_your_real_test_key
FRONTEND_URL=file:///C:/Users/windows%2010/Desktop/Workshop/portfolio/index.html
```

For production on Render, keep `FRONTEND_URL=https://matsoso-portfolio.vercel.app` and use the Render service URL in `DEPLOYED_STRIPE_BACKEND_URL` inside `index.html`.
