INSERT INTO ms_a48c_ec307e2e32e7 (id_universal, fd_client, fd_prefix, fd_product) VALUES
('c52be0fc-d475-425e-8840-01e2b8764224', 'd5cb6795', 'sd', 'Seguridad'),
('53042d47-f6d9-4330-aefc-6cc41043fa45', 'd3ec19c1', 'ms', 'Meta Datos'),
('07374a4a-5529-40d4-9ad0-1d9da6ee2542', 'd0bdc8b6', 'tg', 'Tecnologia'),
('1dea4f1f-7353-4d43-bbd5-d16f71c3c9b1', 'c203af04', 'pm', 'Plataforma') ON DUPLICATE KEY UPDATE id_universal = id_universal;