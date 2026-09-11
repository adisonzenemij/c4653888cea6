INSERT INTO sd_a9da_8e0684f3f419 (id_universal, fd_service) VALUES
('2ac9e780-9142-475e-9926-72501537ada4', 'GET'),
('22f2f0d7-3969-4d64-859d-562828752c58', 'POST'),
('b7c0f396-dfdd-4e7c-bccd-18c865ccf8c5', 'PUT'),
('e4ce5eb5-7ac2-4db9-831e-7839a991c6d3', 'PATCH'),
('0e8feba0-bb0d-44c3-93b7-5408fc76dc5e', 'DELETE') ON DUPLICATE KEY UPDATE id_universal = id_universal;