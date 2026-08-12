# Definition of Done - LabSoft ADN

Un sprint solo se considera cerrado si se cumplen los siguientes criterios:

- [x] Las funcionalidades principales del sprint operan correctamente.
- [x] El código pasa el análisis estático de Pylint sin errores críticos.
- [x] Las plantillas con formularios POST incluyen protección CSRF.
- [ ] No quedan hallazgos de severidad Crítica o Alta sin al menos
      una mitigación en progreso documentada.
- [x] Los cambios en el modelo de datos preservan la integridad
      histórica (on_delete=PROTECT en claves foráneas críticas).
- [ ] El checklist de seguridad OWASP fue revisado antes de integrar
      el código a la rama principal.
