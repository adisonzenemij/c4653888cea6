INSERT INTO pm_bfe4_0a191a6f082d (id_universal, fd_setting) VALUES
('4c5c8071-5166-4980-a5ad-c72d7a98f17d', 'Publico'),
('ca92fde3-6c9e-40fd-b98e-8068cfecb8e1', 'Privado') ON DUPLICATE KEY UPDATE id_universal = id_universal;