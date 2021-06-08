SELECT COUNT(*) FROM aprovacao;
SELECT COUNT(*) FROM aprovacao WHERE tipo='Avaliação do governo federal';
SELECT COUNT(*) FROM aprovacao WHERE tipo='Aprovação do governo federal';
SELECT COUNT(*) FROM aprovacao WHERE presidente='Jair Bolsonaro';
SELECT COUNT(*) FROM aprovacao WHERE presidente='Jair Bolsonaro' AND tipo='Avaliação do governo federal';
SELECT COUNT(*) FROM aprovacao WHERE presidente='Jair Bolsonaro' AND tipo='Aprovação do governo federal';