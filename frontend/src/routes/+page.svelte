<script>
    import { onMount } from 'svelte';
    let resources = [], stats = [], loading = true

    async function fetchStatus() {
        loading = true
        try {
            const response = await fetch('http://localhost:8000/status')
            resources = await response.json()
            await fetchStats()
        } catch (error) {
            console.error('Error:', error)
        }
        loading = false
    }

    async function fetchStats() {
        try {
            const response = await fetch('http://localhost:8000/stats')
            stats = await response.json()
        } catch (error) {
            console.error('Error loading stats:', error)
        }
    }

    onMount(() => {
        fetchStatus()
        const interval = setInterval(fetchStatus, 30000)
        return () => clearInterval(interval)
    })
</script>

<main>
    <div class="container">
        <h1>🌐 Мониторинг сети</h1>
        <button on:click={fetchStatus} disabled={loading}>
            {loading ? 'Loading...' : 'Refresh'}
        </button>
        
        <div class="section">
            <h2>Текущее состояние</h2>
            <div class="sites-list">
                {#each resources as resource}
                    <div class="site-card {resource.status ? 'up' : 'down'}">
                        <h3>{resource.name}</h3>
                        <p>URL: {resource.url}</p>
                        <p>Статус: {resource.status ? '✅ UP' : '❌ DOWN'}</p>
                        {#if resource.response_time}
                            <p>Время отклика: {resource.response_time}ms</p>
                        {/if}
                        {#if resource.error}
                            <p class="error">Ошибка: {resource.error}</p>
                        {/if}
                    </div>
                {/each}
            </div>
        </div>

        {#if stats.length > 0}
            <div class="section">
                <h2>📊 Статистика</h2>
                <div class="stats-grid">
                    {#each stats as stat}
                        <div class="stat-card">
                            <h3>{stat.name}</h3>
                            <div class="stat-item">
                                <span class="stat-label">Работоспособность:</span>
                                <span class="stat-value {stat.uptime > 90 ? 'good' : stat.uptime > 70 ? 'warning' : 'bad'}">
                                    {stat.uptime}%
                                </span>
                            </div>
                            <div class="stat-item">
                                <span class="stat-label">Среднее время:</span>
                                <span class="stat-value">{stat.avg_time}ms</span>
                            </div>
                            <div class="stat-item">
                                <span class="stat-label">Проверки:</span>
                                <span class="stat-value">{stat.total_checks}</span>
                            </div>
                        </div>
                    {/each}
                </div>
            </div>
        {/if}
    </div>
</main>

<style>
    .container { max-width: 800px; margin: 0 auto; padding: 20px; font-family: Arial; }
    .section { margin-bottom: 30px; }
    h1, h2 { color: #333; text-align: center; }
    h2 { border-bottom: 2px solid #eee; padding-bottom: 10px; margin-bottom: 20px; }
    button {padding: 10px 20px; background: #007acc; color: white; border: none; border-radius: 5px; cursor: pointer; margin-bottom: 20px; display: block; margin: 0 auto; font-size: 16px; transition: background 0.3s;}
    button:disabled { background: #ccc; cursor: not-allowed; }
    button:hover:not(:disabled) { background: #0e5b8f; }
    .sites-list { display: flex; flex-direction: column; gap: 15px; }
    .site-card { padding: 20px; border-radius: 10px; border: 2px solid #ddd; transition: transform 0.2s; }
    .site-card:hover { transform: translateY(-2px); box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
    .up { border-color: #28a745; background: linear-gradient(135deg, #f0fff0, #e0ffe0); }
    .down { border-color: #dc3545; background: linear-gradient(135deg, #fff0f0, #ffe0e0); }
    .error { background: #ffe6e6; border: 1px solid #ff4444; padding: 10px; border-radius: 6px; color: #cc0000; margin-top: 10px; font-size: 14px; }
    .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; }
    .stat-card { padding: 20px; border: 1px solid #ddd; border-radius: 10px; background: linear-gradient(135deg, #f9f9f9, #f0f0f0); box-shadow: 0 2px 4px rgba(0,0,0,0.1); transition: transform 0.2s; }
    .stat-card:hover { transform: translateY(-2px); box-shadow: 0 4px 8px rgba(0,0,0,0.15); }
    .stat-card h3 { margin: 0 0 15px 0; text-align: center; color: #333; font-size: 18px; }
    .stat-item { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
    .stat-label { font-weight: bold; color: #666; font-size: 14px; }
    .stat-value { font-weight: bold; font-size: 14px; }
    .stat-value.good { color: #28a745; }
    .stat-value.warning { color: #ffc107; }
    .stat-value.bad { color: #dc3545; }
    h3 { margin: 0 0 10px 0; font-size: 20px; }
    p { margin: 8px 0; color: #555; }
    .site-card h3 { color: #333; margin-bottom: 15px; }
    .site-card p { margin: 5px 0; }
</style>