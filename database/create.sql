CREATE DATABASE empresa_quimica;

CREATE TABLE wishlist (
    id INT(11) NOT NULL AUTO_INCREMENT,
    usuario_id INT(11) NOT NULL,
    producto_id INT(11) NOT NULL,
    PRIMARY KEY (id),
    KEY (usuario_id),
    KEY (producto_id)
);