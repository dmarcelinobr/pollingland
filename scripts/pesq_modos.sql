SELECT COUNT(modo) FROM aprovacao;
SELECT COUNT(*) FROM aprovacao WHERE modo='FF';
SELECT COUNT(*) FROM aprovacao WHERE modo='CATI';
SELECT COUNT(*) FROM aprovacao WHERE modo='IRV';
SELECT COUNT(*) FROM aprovacao WHERE modo='Online';

SELECT COUNT(*) FROM aprovacao WHERE presidente='Jair Bolsonaro' AND modo='FF';
SELECT COUNT(*) FROM aprovacao WHERE presidente='Jair Bolsonaro' AND modo='CATI';
SELECT COUNT(*) FROM aprovacao WHERE presidente='Jair Bolsonaro' AND modo='IRV';
SELECT COUNT(*) FROM aprovacao WHERE presidente='Jair Bolsonaro' AND modo='Online';