INSERT INTO sd_a1bb_a6baddf4c35a (id_universal, fd_service) VALUES
('aa72f330-f7b3-4cca-a6ff-a73e7cda780a', 'http://localhost:4200'),
('0480162b-f665-49a7-9962-551b45e4bb82', 'http://127.0.0.1:4200'),
('13a40bd4-9a77-459a-b914-3a716f816321', 'https://d03f3062e3cf.datacompute.org'),
('06456ce1-0fc6-4bce-9fe3-8d649b8e0135', 'https://cun-dis38.datacompute.org') ON DUPLICATE KEY UPDATE id_universal = id_universal;