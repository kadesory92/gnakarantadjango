document.getElementById('sidebarToggle').addEventListener('click', function() {
    var sidebar = document.getElementById('sidebar');
    var mainContent = document.getElementById('main-content');
    sidebar.classList.toggle('collapsed');
    if (mainContent.classList.contains('col-lg-10')) {
      mainContent.classList.remove('col-lg-10');
      mainContent.classList.add('col-lg-12');
    } else {
      mainContent.classList.remove('col-lg-12');
      mainContent.classList.add('col-lg-10');
    }
  });