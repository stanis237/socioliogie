import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import App from '../App';
import { rest } from 'msw';
import { setupServer } from 'msw/node';

// Mock backend responses
const server = setupServer(
  rest.post('/api/users/signup/', (req, res, ctx) => {
    const { email, password, password_confirm, first_name, last_name } = req.body as any;
    if (password !== password_confirm) {
      return res(ctx.status(400), ctx.json({ password: ["Les mots de passe ne correspondent pas."] }));
    }
    return res(
      ctx.status(201),
      ctx.json({
        access: 'mock_access_token',
        refresh: 'mock_refresh_token',
        user: { id: '123', email, first_name, last_name },
      })
    );
  }),
  rest.post('/api/users/login/', (req, res, ctx) => {
    const { email, password } = req.body as any;
    if (email === 'testuser@example.com' && password === 'StrongPassw0rd!') {
      return res(
        ctx.status(200),
        ctx.json({
          access: 'mock_access_token',
          refresh: 'mock_refresh_token',
          user: { id: '123', email, first_name: 'Test', last_name: 'User' },
        })
      );
    }
    return res(ctx.status(401), ctx.json({ error: 'Identifiants invalides' }));
  }),
  rest.get('/api/users/profile/', (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json({
        id: '123',
        email: 'testuser@example.com',
        first_name: 'Test',
        last_name: 'User',
      })
    );
  })
);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

test('Flux complet utilisateur: inscription, connexion et accès dashboard', async () => {
  render(<App />);

  // Naviguer vers la page d'inscription
  const signupLink = screen.getByText(/Inscription/i);
  fireEvent.click(signupLink);

  // Remplir les champs d'inscription
  fireEvent.change(screen.getByLabelText(/Email/i), { target: { value: 'testuser@example.com' } });
  fireEvent.change(screen.getByLabelText(/Prénom/i), { target: { value: 'Test' } });
  fireEvent.change(screen.getByLabelText(/Nom/i), { target: { value: 'User' } });
  fireEvent.change(screen.getByLabelText(/^Mot de passe$/i), { target: { value: 'StrongPassw0rd!' } });
  fireEvent.change(screen.getByLabelText(/Confirmer le mot de passe/i), { target: { value: 'StrongPassw0rd!' } });

  const submitButton = screen.getByRole('button', { name: /S'inscrire/i });
  fireEvent.click(submitButton);

  // Attendre que la redirection vers le dashboard ait lieu
  await waitFor(() => expect(screen.getByText(/Tableau de bord/i)).toBeInTheDocument());

  // Déconnexion
  const logoutButton = screen.getByText(/Déconnexion/i);
  fireEvent.click(logoutButton);

  // Naviguer vers la page de connexion
  const loginLink = screen.getByText(/Connexion/i);
  fireEvent.click(loginLink);

  // Remplir les champs de connexion
  fireEvent.change(screen.getByLabelText(/Email/i), { target: { value: 'testuser@example.com' } });
  fireEvent.change(screen.getByLabelText(/Mot de passe/i), { target: { value: 'StrongPassw0rd!' } });
  const loginButton = screen.getByRole('button', { name: /Se connecter/i });
  fireEvent.click(loginButton);

  // Vérifier affichage du tableau de bord après connexion
  await waitFor(() => expect(screen.getByText(/Tableau de bord/i)).toBeInTheDocument());
});
