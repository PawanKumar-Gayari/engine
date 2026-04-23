<?php
/*
Plugin Name: AI Content Generator
Description: Generate posts using your AI engine
Version: 1.0
*/

// 🔥 MENU ADD
add_action('admin_menu', function () {
    add_menu_page(
        'AI Generator',
        'AI Generator',
        'manage_options',
        'ai-generator',
        'ai_generator_page'
    );
});

// 🔥 SETTINGS SAVE
if (isset($_POST['save_settings'])) {
    update_option('ai_api_key', sanitize_text_field($_POST['api_key']));
    update_option('ai_api_url', sanitize_text_field($_POST['api_url']));
}

// 🔥 GENERATE POST
if (isset($_POST['generate_post'])) {

    $keyword = sanitize_text_field($_POST['keyword']);
    $api_key = get_option('ai_api_key');
    $api_url = get_option('ai_api_url');

    $response = wp_remote_post($api_url, array(
        'headers' => array(
            'Content-Type' => 'application/json',
            'x-api-key' => $api_key
        ),
        'body' => json_encode(array(
            'keyword' => $keyword
        ))
    ));

    if (!is_wp_error($response)) {

        $body = wp_remote_retrieve_body($response);
        $data = json_decode($body, true);

        if (isset($data['title'])) {

            wp_insert_post(array(
                'post_title'   => $data['title'],
                'post_content' => 'Generated via AI Engine',
                'post_status'  => 'publish'
            ));

            echo "<div class='updated'><p>Post Generated Successfully!</p></div>";
        }
    } else {
        echo "<div class='error'><p>API Error!</p></div>";
    }
}

// 🔥 ADMIN PAGE UI
function ai_generator_page() {
    ?>

    <div class="wrap">
        <h1>🚀 AI Content Generator</h1>

        <form method="post">
            <h2>🔑 API Settings</h2>

            <input type="text" name="api_url" placeholder="API URL"
                value="<?php echo esc_attr(get_option('ai_api_url')); ?>" style="width:400px;"><br><br>

            <input type="text" name="api_key" placeholder="API Key"
                value="<?php echo esc_attr(get_option('ai_api_key')); ?>" style="width:400px;"><br><br>

            <button type="submit" name="save_settings" class="button button-primary">
                Save Settings
            </button>
        </form>

        <hr>

        <form method="post">
            <h2>📝 Generate Post</h2>

            <input type="text" name="keyword" placeholder="Enter keyword"
                style="width:400px;" required><br><br>

            <button type="submit" name="generate_post" class="button button-primary">
                Generate & Publish
            </button>
        </form>

    </div>

    <?php
}